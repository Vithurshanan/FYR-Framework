"""
Energy-Efficient Container Consolidation Framework - Streamlit Dashboard

This dashboard provides real-time visualization of:
- Host status and resource utilization
- Energy consumption trends
- Container distribution across hosts
- Migration events and consolidation decisions
- Performance KPIs and efficiency metrics

Author: Ananthakumar Vithurshanan
Year: 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
import io
from openpyxl import Workbook
from openpyxl.chart import LineChart, BarChart, Reference
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Timezone support for Sri Lanka (Colombo) - UTC+5:30
try:
    from zoneinfo import ZoneInfo
    SRI_LANKA_TZ = ZoneInfo("Asia/Colombo")
except ImportError:
    # Fallback for older Python versions
    try:
        import pytz
        SRI_LANKA_TZ = pytz.timezone("Asia/Colombo")
    except ImportError:
        # If neither is available, use UTC offset manually
        from datetime import timedelta, timezone
        SRI_LANKA_TZ = timezone(timedelta(hours=5, minutes=30))


def get_sri_lanka_time():
    """Get current time in Sri Lanka (Colombo) timezone."""
    return datetime.now(SRI_LANKA_TZ)


def format_sri_lanka_time(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """Format datetime to Sri Lanka timezone string."""
    if dt is None:
        return "N/A"
    
    # If datetime is timezone-naive, assume it's UTC and convert
    if dt.tzinfo is None:
        if isinstance(dt, pd.Timestamp):
            dt = dt.tz_localize('UTC')
        else:
            dt = dt.replace(tzinfo=timezone.utc)
    
    # Convert to Sri Lanka timezone
    if isinstance(dt, pd.Timestamp):
        dt_sl = dt.tz_convert('Asia/Colombo')
    else:
        dt_sl = dt.astimezone(SRI_LANKA_TZ)
    
    return dt_sl.strftime(format_str)

# Page configuration
st.set_page_config(
    page_title="Energy Framework Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Sticky header section */
    .sticky-header {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(14, 17, 23, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #2ecc71;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2ecc71;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1e3c72 0%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .subtitle {
        text-align: center;
        color: #ecf0f1;
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: 300;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ecc71;
    }
    .status-active {
        color: #2ecc71;  /* Green for active */
        font-weight: bold;
    }
    .status-idle {
        color: #f39c12;  /* Orange/Yellow for idle */
        font-weight: bold;
    }
    .status-shutdown {
        color: #f39c12;  /* Orange/Yellow for shutdown (changed from red) */
        font-weight: bold;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Ensure content doesn't overlap with sticky header */
    .main-content {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


class DashboardDataLoader:
    """Handles data loading and processing from framework outputs."""
    
    def __init__(self, output_dir: str = None):
        """Initialize data loader with output directory."""
        # If no output_dir specified, use relative to dashboard.py location
        if output_dir is None:
            # Get the directory where dashboard.py is located
            dashboard_dir = Path(__file__).parent
            # Go up one level to energy_framework, then to output
            self.output_dir = dashboard_dir.parent / "output"
        else:
            self.output_dir = Path(output_dir)
        
        self.csv_path = self.output_dir / "energy_log.csv"
        self.json_path = self.output_dir / "energy_log.json"
        self.kpis_path = self.output_dir / "reports" / "kpis.json"
    
    def load_csv_data(_self, force_reload: bool = False) -> pd.DataFrame:
        """Load energy log CSV without caching to show real-time data."""
        try:
            # Initialize session state for tracking file modifications
            if 'last_file_mtime' not in st.session_state:
                st.session_state['last_file_mtime'] = 0
            if 'last_file_size' not in st.session_state:
                st.session_state['last_file_size'] = 0
            
            # Debug: Show the path being used
            csv_abs_path = _self.csv_path.absolute()
            
            if _self.csv_path.exists():
                # Check file modification time and size to detect changes
                file_mtime = os.path.getmtime(_self.csv_path)
                file_size = os.path.getsize(_self.csv_path)
                time_since_update = time.time() - file_mtime
                
                # Detect if file has changed
                file_changed = (
                    force_reload or
                    file_mtime != st.session_state.get('last_file_mtime') or
                    file_size != st.session_state.get('last_file_size')
                )
                
                # Update session state
                st.session_state['last_file_mtime'] = file_mtime
                st.session_state['last_file_size'] = file_size
                
                # Read CSV file - always read fresh (no caching)
                # Use low_memory=False to ensure we get all data
                df = pd.read_csv(_self.csv_path, low_memory=False)
                
                if len(df) > 0:
                    # Parse datetime and convert to Sri Lanka timezone
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    # If datetime is timezone-naive, assume UTC and convert to Sri Lanka time
                    if df['datetime'].dt.tz is None:
                        df['datetime'] = df['datetime'].dt.tz_localize('UTC')
                    df['datetime'] = df['datetime'].dt.tz_convert('Asia/Colombo')
                    
                    # Rename columns to match expected format
                    if 'cores' in df.columns:
                        df = df.rename(columns={'cores': 'cpu_cores'})
                    if 'ram_gb' in df.columns:
                        df = df.rename(columns={'ram_gb': 'memory_gb'})
                    if 'temperature_c' in df.columns:
                        df = df.rename(columns={'temperature_c': 'temperature_celsius'})
                    
                    # Handle missing latency and throughput columns
                    if 'latency_ms' not in df.columns:
                        df['latency_ms'] = np.nan
                    if 'throughput_mbps' not in df.columns:
                        df['throughput_mbps'] = np.nan
                    
                    # Show data freshness indicator with change status
                    status_icon = "🔄" if file_changed else "✅"
                    if time_since_update < 5:
                        st.sidebar.success(f"{status_icon} Loaded {len(df)} data points (LIVE - {int(time_since_update)}s ago)")
                    elif time_since_update < 30:
                        st.sidebar.info(f"{status_icon} Loaded {len(df)} data points ({int(time_since_update)}s ago)")
                    else:
                        st.sidebar.warning(f"⚠️ Loaded {len(df)} data points (STALE - {int(time_since_update)}s ago)")
                    
                    # Show latest timestamp in Sri Lanka timezone
                    latest_time = df['datetime'].iloc[-1]
                    latest_time_str = format_sri_lanka_time(latest_time, '%Y-%m-%d %H:%M:%S')
                    st.sidebar.write(f"**Latest Data:** {latest_time_str} (SLT)")
                    
                    # Store in session state for comparison
                    st.session_state['last_df_size'] = len(df)
                    st.session_state['last_df_timestamp'] = str(latest_time)
                    
                    return df
                else:
                    st.sidebar.warning("⚠️ CSV file is empty")
                    return _self._generate_sample_data()
            else:
                st.sidebar.warning("⚠️ CSV file not found, using sample data")
                st.sidebar.write(f"**Expected path:** {csv_abs_path}")
                return _self._generate_sample_data()
        except Exception as e:
            st.sidebar.error(f"❌ Error loading CSV: {e}")
            import traceback
            st.sidebar.error(f"**Traceback:** {traceback.format_exc()}")
            st.sidebar.warning("⚠️ Falling back to sample data")
            return _self._generate_sample_data()
    
    def load_kpis(_self) -> dict:
        """Load KPIs from JSON."""
        try:
            if _self.kpis_path.exists():
                with open(_self.kpis_path, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            st.error(f"Error loading KPIs: {e}")
            return {}
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate sample data for demo purposes."""
        np.random.seed(42)
        timestamps = pd.date_range(start='2025-01-01', periods=50, freq='10s')
        
        data = []
        for i, ts in enumerate(timestamps):
            for host_id in ['host-001', 'host-002', 'host-003', 'host-004', 'host-005']:
                data.append({
                    'timestamp': ts.timestamp(),
                    'datetime': ts,
                    'host_id': host_id,
                    'cpu_utilization': np.random.uniform(0.3, 0.9),
                    'memory_utilization': np.random.uniform(0.4, 0.8),
                    'cpu_cores': 8,
                    'memory_gb': 16.0,
                    'power_watts': np.random.uniform(100, 250),
                    'temperature_celsius': np.random.uniform(50, 80),
                    'active_containers': np.random.randint(0, 5),
                    'state': 'active' if np.random.random() > 0.2 else 'shutdown',
                    'is_idle': False,
                    'latency_ms': np.random.uniform(10, 60),
                    'throughput_mbps': np.random.uniform(100, 500)
                })
        
        return pd.DataFrame(data)


def render_header():
    """Render dashboard header."""
    st.markdown('''
    <div class="sticky-header">
        <h1 class="main-header">🌱 Energy-Efficient Container Consolidation Dashboard</h1>
        <div class="subtitle">Real-Time Visualization of Sustainable Cloud Infrastructure</div>
    </div>
    ''', unsafe_allow_html=True)


def render_sidebar(data_loader: DashboardDataLoader):
    """Render sidebar with controls and settings."""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150/2ecc71/ffffff?text=Energy+Framework", 
                 use_column_width=True)
        
        st.markdown("## ⚙️ Dashboard Controls")
        
        # Real-time status with full timestamp and update counter
        st.markdown("### 🟢 Real-Time Status")
        
        # Initialize refresh counter in session state
        if 'refresh_count' not in st.session_state:
            st.session_state['refresh_count'] = 0
        if 'last_refresh_time' not in st.session_state:
            st.session_state['last_refresh_time'] = get_sri_lanka_time()
        
        # Increment refresh counter on each page load
        st.session_state['refresh_count'] = st.session_state.get('refresh_count', 0) + 1
        st.session_state['last_refresh_time'] = get_sri_lanka_time()
        
        current_time = get_sri_lanka_time().strftime("%Y-%m-%d %H:%M:%S")
        refresh_count = st.session_state['refresh_count']
        last_refresh = st.session_state['last_refresh_time'].strftime("%H:%M:%S")
        
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(46, 204, 113, 0.1); border-radius: 5px; margin: 10px 0;">
            <span style="color: #2ecc71; font-weight: bold; font-size: 18px;">🟢 LIVE</span><br>
            <span class="live-clock" style="color: #ecf0f1; font-size: 12px; font-family: monospace;">Loading...</span><br>
            <span style="color: #95a5a6; font-size: 11px;">Updates: {refresh_count} | Last: {last_refresh}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Refresh settings
        st.markdown("### 🔄 Refresh Settings")
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 1, 10, 2, help="How often the dashboard automatically updates (1-10 seconds)")
        
        if st.button("🔄 Refresh Now", use_container_width=True):
            # Clear all caches and force reload
            st.cache_data.clear()
            st.session_state['force_reload'] = True
            if 'last_file_mtime' in st.session_state:
                del st.session_state['last_file_mtime']
            if 'last_file_size' in st.session_state:
                del st.session_state['last_file_size']
            if 'file_check_mtime' in st.session_state:
                del st.session_state['file_check_mtime']
            st.rerun()
        
        if st.button("🗑️ Clear Cache & Reload", use_container_width=True):
            # Clear all caches and session state
            st.cache_data.clear()
            st.session_state['force_reload'] = True
            if 'last_file_mtime' in st.session_state:
                del st.session_state['last_file_mtime']
            if 'last_file_size' in st.session_state:
                del st.session_state['last_file_size']
            if 'file_check_mtime' in st.session_state:
                del st.session_state['file_check_mtime']
            if 'last_df_size' in st.session_state:
                del st.session_state['last_df_size']
            if 'last_df_timestamp' in st.session_state:
                del st.session_state['last_df_timestamp']
            st.success("Cache cleared! Reloading data...")
            st.rerun()
        
        st.markdown("---")
        
        # Data status with debug info
        st.markdown("### 📊 Data Status")
        csv_exists = data_loader.csv_path.exists()
        st.write(f"**CSV Log:** {'✅ Found' if csv_exists else '⚠️ Sample Data'}")
        
        if csv_exists:
            file_size = os.path.getsize(data_loader.csv_path) / 1024
            st.write(f"**File Size:** {file_size:.2f} KB")
            mod_time = datetime.fromtimestamp(os.path.getmtime(data_loader.csv_path), tz=timezone.utc)
            mod_time_sl = format_sri_lanka_time(mod_time, '%H:%M:%S')
            st.write(f"**Last Updated:** {mod_time_sl} (SLT)")
            
            # Show data preview
            try:
                df = pd.read_csv(data_loader.csv_path)
                st.write(f"**Data Points:** {len(df)}")
                latest_dt = df['datetime'].iloc[-1] if len(df) > 0 else None
                latest_time_str = format_sri_lanka_time(latest_dt, '%H:%M:%S') if latest_dt is not None else 'N/A'
                st.write(f"**Latest Time:** {latest_time_str} (SLT)")
                st.write(f"**Total Power:** {df['power_watts'].sum():.0f}W" if len(df) > 0 else "N/A")
            except Exception as e:
                st.write(f"**Error:** {str(e)}")
        
        st.markdown("---")
        
        # Info
        st.markdown("### ℹ️ About")
        st.info("""
        This dashboard visualizes real-time metrics from the Energy-Efficient 
        Container Consolidation Framework.
        
        **Features:**
        - Live host monitoring
        - Energy consumption tracking
        - Container distribution
        - Migration events
        - Performance KPIs
        - Latency and Throughput metrics
        - Excel export with graphs
        """)
        
        st.markdown("---")
        
        # Export to Excel button
        st.markdown("### 📥 Export Data")
        if st.button("📊 Export to Excel with Graphs", use_container_width=True):
            st.session_state['export_excel'] = True
        
        return auto_refresh, refresh_interval


def render_metrics_overview(df: pd.DataFrame, kpis: dict):
    """Render key metrics overview with real-time updates."""
    st.markdown("## 📊 System Overview")
    
    # Real-time status indicator with dynamic time and data source (Sri Lanka timezone)
    current_time = get_sri_lanka_time().strftime("%Y-%m-%d %H:%M:%S")
    data_source = "REAL DATA" if not df.empty and len(df) > 100 else "SAMPLE DATA"
    data_color = "#2ecc71" if data_source == "REAL DATA" else "#f39c12"
    
    # Get auto-refresh status
    auto_refresh_status = "ENABLED" if st.session_state.get('auto_refresh', True) else "DISABLED"
    refresh_interval = st.session_state.get('refresh_interval', 2)
    refresh_count = st.session_state.get('refresh_count', 0)
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px; padding: 15px; background: rgba(46, 204, 113, 0.05); border-radius: 8px; border: 2px solid rgba(46, 204, 113, 0.3);">
        <span style="color: #2ecc71; font-weight: bold; font-size: 18px;">🟢 LIVE MONITORING</span><br>
        <span style="color: #ecf0f1; margin-left: 10px; font-size: 14px;">Current Time (SLT): {current_time}</span><br>
        <span style="color: {data_color}; font-weight: bold; font-size: 14px;">📊 {data_source}</span><br>
        <span style="color: #3498db; font-size: 12px;">🔄 Auto-Refresh: {auto_refresh_status} (every {refresh_interval}s) | Total Updates: {refresh_count}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a live timestamp that updates with JavaScript
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 10px; background: rgba(46, 204, 113, 0.1); border-radius: 5px; margin: 10px 0;">
            <span style="color: #2ecc71; font-weight: bold; font-size: 16px;">🕐 LIVE TIMESTAMP</span><br>
            <span class="live-clock" style="color: #ecf0f1; font-size: 14px; font-family: monospace;">Loading...</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Get latest data and show data freshness
    if not df.empty:
        latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()]
        
        # Show data freshness in Sri Lanka timezone
        latest_timestamp = df['datetime'].max()
        latest_timestamp_str = format_sri_lanka_time(latest_timestamp, '%Y-%m-%d %H:%M:%S')
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="color: #3498db; font-size: 12px;">📊 Data Last Updated: {latest_timestamp_str} (SLT)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate real-time metrics
        total_power = latest['power_watts'].sum()
        avg_cpu = latest['cpu_utilization'].mean() * 100
        avg_memory = latest['memory_utilization'].mean() * 100
        active_hosts = (latest['state'] == 'active').sum()
        total_containers = latest['active_containers'].sum()
        
        # Calculate trends (compare with previous data point)
        if len(df) > 1:
            prev_data = df.groupby('host_id').nth(-2)
            prev_power = prev_data['power_watts'].sum()
            prev_cpu = prev_data['cpu_utilization'].mean() * 100
            prev_memory = prev_data['memory_utilization'].mean() * 100
            prev_containers = prev_data['active_containers'].sum()
            
            power_trend = total_power - prev_power
            cpu_trend = avg_cpu - prev_cpu
            memory_trend = avg_memory - prev_memory
            container_trend = total_containers - prev_containers
        else:
            power_trend = cpu_trend = memory_trend = container_trend = 0
        
        # Display metrics with trends
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="💡 Total Power",
                value=f"{total_power:.0f} W",
                delta=f"{power_trend:+.0f} W" if power_trend != 0 else "0 W"
            )
        
        with col2:
            st.metric(
                label="🖥️ Active Hosts",
                value=f"{active_hosts}",
                delta=f"{len(latest) - active_hosts} shutdown"
            )
        
        with col3:
            st.metric(
                label="📦 Containers",
                value=f"{total_containers}",
                delta=f"{container_trend:+d}" if container_trend != 0 else "0"
            )
        
        with col4:
            st.metric(
                label="⚡ Avg CPU",
                value=f"{avg_cpu:.1f}%",
                delta=f"{cpu_trend:+.1f}%" if cpu_trend != 0 else "0%"
            )
        
        with col5:
            st.metric(
                label="💾 Avg Memory",
                value=f"{avg_memory:.1f}%",
                delta=f"{memory_trend:+.1f}%" if memory_trend != 0 else "0%"
            )
        
        # Add environmental impact metrics
        st.markdown("---")
        st.markdown("### 🌱 Environmental Impact")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate environmental metrics
        carbon_footprint = (total_power * 0.0005) / 1000  # kg CO2 per kWh
        estimated_cost = (total_power * 0.12) / 1000  # $0.12 per kWh
        efficiency_score = (1 - (total_power / (active_hosts * 200))) * 100  # Efficiency percentage
        
        with col1:
            st.metric(
                label="🌍 Carbon Footprint",
                value=f"{carbon_footprint:.4f} kg CO₂",
                delta="Real-time"
            )
        
        with col2:
            st.metric(
                label="💰 Estimated Cost",
                value=f"${estimated_cost:.4f}",
                delta="Per hour"
            )
        
        with col3:
            st.metric(
                label="⚡ Efficiency Score",
                value=f"{efficiency_score:.1f}%",
                delta="Energy efficiency"
            )
        
        with col4:
            st.metric(
                label="📊 Data Points",
                value=f"{len(df)}",
                delta="Total collected"
            )


def render_host_overview(df: pd.DataFrame):
    """Render detailed host status overview."""
    st.markdown("## 🖥️ Host Status Overview")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Get latest data for each host (most recent timestamp)
    latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()].reset_index(drop=True)
    
    # Debug: Show what data we're using
    st.sidebar.markdown("### 🖥️ Host Data Debug")
    for _, host in latest.iterrows():
        st.sidebar.write(f"**{host['host_id']}**: CPU {host['cpu_utilization']*100:.1f}%, Power {host['power_watts']:.0f}W, Containers {host['active_containers']}")
    st.sidebar.markdown("---")
    
    # Create columns for hosts
    num_hosts = len(latest)
    cols = st.columns(min(num_hosts, 3))
    
    for idx, (_, host) in enumerate(latest.iterrows()):
        with cols[idx % 3]:
            # Determine status color based on state
            # ACTIVE = GREEN, NOT ACTIVE (shutdown/idle) = YELLOW/ORANGE
            if host['state'] == 'active':
                status_class = "status-active"
                status_icon = "🟢"
                status_color = "#2ecc71"  # Green
            elif host['state'] == 'shutdown':
                status_class = "status-shutdown"
                status_icon = "🟡"
                status_color = "#f39c12"  # Orange/Yellow
            else:
                # Handle idle or any other state as yellow/orange
                status_class = "status-idle"
                status_icon = "🟡"
                status_color = "#f39c12"  # Orange/Yellow
            
            st.markdown(f"### {status_icon} {host['host_id']}")
            
            # Status with correct color
            st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{host['state'].upper()}</span>", 
                       unsafe_allow_html=True)
            
            # Specs
            st.write(f"**Specs:** {host['cpu_cores']} cores, {host['memory_gb']:.0f}GB RAM")
            
            # Metrics
            if host['state'] == 'active':
                st.progress(host['cpu_utilization'], text=f"CPU: {host['cpu_utilization']*100:.1f}%")
                st.progress(host['memory_utilization'], text=f"Memory: {host['memory_utilization']*100:.1f}%")
                st.write(f"⚡ Power: **{host['power_watts']:.0f} W**")
                st.write(f"🌡️ Temp: **{host['temperature_celsius']:.1f}°C**")
                st.write(f"📦 Containers: **{host['active_containers']}**")
            else:
                st.write("💤 Host is shut down")
            
            st.markdown("---")


def render_energy_consumption(df: pd.DataFrame):
    """Render energy consumption charts."""
    st.markdown("## 💡 Energy Consumption Analysis")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Total power over time
    power_by_time = df.groupby('datetime')['power_watts'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=power_by_time['datetime'],
        y=power_by_time['power_watts'],
        mode='lines+markers',
        name='Total Power',
        line=dict(color='#2ecc71', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))
    
    fig.update_layout(
        title="Cluster Power Consumption Over Time",
        xaxis_title="Time",
        yaxis_title="Power (W)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Power per host
    st.markdown("### Power Distribution by Host")
    
    fig2 = px.line(
        df[df['state'] == 'active'],
        x='datetime',
        y='power_watts',
        color='host_id',
        title='Power Consumption per Host',
        labels={'power_watts': 'Power (W)', 'datetime': 'Time'},
        template='plotly_white'
    )
    
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)


def render_container_distribution(df: pd.DataFrame):
    """Render container distribution charts."""
    st.markdown("## 📦 Container Distribution")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Latest distribution
    latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()].reset_index(drop=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = px.bar(
            latest,
            x='host_id',
            y='active_containers',
            color='state',
            title='Current Container Distribution',
            labels={'active_containers': 'Containers', 'host_id': 'Host'},
            color_discrete_map={'active': '#2ecc71', 'shutdown': '#f39c12', 'idle': '#f39c12'},  # Green for active, Orange/Yellow for shutdown/idle
            template='plotly_white'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart
        active_hosts = latest[latest['state'] == 'active']
        fig2 = px.pie(
            active_hosts,
            values='active_containers',
            names='host_id',
            title='Container Distribution (Active Hosts)',
            template='plotly_white'
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Timeline
    st.markdown("### Container Count Over Time")
    
    container_timeline = df.groupby(['datetime', 'host_id'])['active_containers'].sum().reset_index()
    
    fig3 = px.area(
        container_timeline,
        x='datetime',
        y='active_containers',
        color='host_id',
        title='Container Count Timeline',
        labels={'active_containers': 'Containers', 'datetime': 'Time'},
        template='plotly_white'
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)


def render_utilization_trends(df: pd.DataFrame):
    """Render resource utilization trends."""
    st.markdown("## 📈 Resource Utilization Trends")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('CPU Utilization', 'Memory Utilization'),
        vertical_spacing=0.15
    )
    
    # CPU utilization
    for host_id in df['host_id'].unique():
        host_data = df[df['host_id'] == host_id]
        fig.add_trace(
            go.Scatter(
                x=host_data['datetime'],
                y=host_data['cpu_utilization'] * 100,
                mode='lines',
                name=f'{host_id} CPU',
                legendgroup=host_id
            ),
            row=1, col=1
        )
    
    # Memory utilization
    for host_id in df['host_id'].unique():
        host_data = df[df['host_id'] == host_id]
        fig.add_trace(
            go.Scatter(
                x=host_data['datetime'],
                y=host_data['memory_utilization'] * 100,
                mode='lines',
                name=f'{host_id} Mem',
                legendgroup=host_id,
                showlegend=False
            ),
            row=2, col=1
        )
    
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="CPU %", row=1, col=1)
    fig.update_yaxes(title_text="Memory %", row=2, col=1)
    
    fig.update_layout(
        height=600,
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_kpi_summary(kpis: dict, df: pd.DataFrame):
    """Render KPI summary cards."""
    st.markdown("## 🎯 Performance KPIs")
    
    # Calculate KPIs from current data if KPI file is missing or incomplete
    if not kpis or not df.empty:
        # Get latest data for each host
        if not df.empty:
            latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()].reset_index(drop=True)
            
            # Calculate KPIs from current data
            total_power = float(latest['power_watts'].sum())
            avg_power = float(latest['power_watts'].mean())
            total_containers = int(latest['active_containers'].sum())
            active_hosts = int((latest['state'] == 'active').sum())
            total_hosts = int(len(latest))
            
            # Calculate average CPU/Memory (already in decimal form, convert to percentage)
            avg_cpu_pct = float(latest['cpu_utilization'].mean() * 100)
            avg_mem_pct = float(latest['memory_utilization'].mean() * 100)
            
            # Calculate derived metrics
            power_per_container = (avg_power / total_containers) if total_containers > 0 else 0.0
            containers_per_host = (total_containers / total_hosts) if total_hosts > 0 else 0.0
            
            # Calculate total energy (approximate: average power * time in hours)
            # For real-time monitoring, estimate based on average power
            # Assuming 1 hour of operation for estimation
            total_energy_wh = avg_power * 1.0  # Watts * hours = Wh
            
            # Use calculated values or fall back to KPI file values
            total_energy_wh = kpis.get('total_energy_wh', total_energy_wh) if kpis else total_energy_wh
            avg_power = kpis.get('average_power_watts', kpis.get('total_power_watts', avg_power)) if kpis else avg_power
            total_containers = kpis.get('total_containers', total_containers) if kpis else total_containers
            total_hosts = kpis.get('total_hosts', total_hosts) if kpis else total_hosts
            active_hosts = kpis.get('active_hosts', active_hosts) if kpis else active_hosts
            
            # CPU/Memory: Check if already in percentage (from JSON) or needs conversion
            if kpis and 'average_cpu_utilization' in kpis:
                # JSON already has percentage, use as-is
                avg_cpu_pct = float(kpis['average_cpu_utilization'])
            if kpis and 'average_memory_utilization' in kpis:
                # JSON already has percentage, use as-is
                avg_mem_pct = float(kpis['average_memory_utilization'])
            
            metrics_collected = kpis.get('total_data_points', kpis.get('metrics_collected', len(df))) if kpis else len(df)
        else:
            # No data available, use KPI file or defaults
            total_energy_wh = kpis.get('total_energy_wh', 0) if kpis else 0
            avg_power = kpis.get('average_power_watts', kpis.get('total_power_watts', 0)) if kpis else 0
            total_containers = kpis.get('total_containers', 0) if kpis else 0
            total_hosts = kpis.get('total_hosts', 0) if kpis else 0
            active_hosts = kpis.get('active_hosts', 0) if kpis else 0
            avg_cpu_pct = kpis.get('average_cpu_utilization', 0) if kpis else 0
            avg_mem_pct = kpis.get('average_memory_utilization', 0) if kpis else 0
            power_per_container = (avg_power / total_containers) if total_containers > 0 else 0.0
            containers_per_host = (total_containers / total_hosts) if total_hosts > 0 else 0.0
            metrics_collected = kpis.get('total_data_points', kpis.get('metrics_collected', 0)) if kpis else 0
    
    # Main KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ⚡ Energy Metrics")
        st.metric("Total Energy", f"{total_energy_wh:.2f} Wh")
        st.metric("Average Power", f"{avg_power:.2f} W")
        st.metric("Power per Container", f"{power_per_container:.2f} W")
    
    with col2:
        st.markdown("### 🖥️ Host Metrics")
        st.metric("Total Hosts", total_hosts)
        st.metric("Avg Active Hosts", f"{active_hosts:.1f}")
        
        if kpis and 'consolidation_statistics' in kpis:
            energy_saved = kpis['consolidation_statistics'].get('total_energy_saved_watts', 0)
            st.metric("Energy Saved", f"{energy_saved:.2f} W", delta=f"{energy_saved:.1f}W")
    
    with col3:
        st.markdown("### 📦 Workload Stats")
        st.metric("Total Containers", total_containers)
        st.metric("Containers/Host", f"{containers_per_host:.2f}")
        
        if kpis and 'migration_statistics' in kpis:
            migrations = kpis['migration_statistics'].get('total_migrations', 0)
            st.metric("Total Migrations", migrations)
    
    with col4:
        st.markdown("### 📊 Utilization")
        st.metric("Avg CPU Usage", f"{avg_cpu_pct:.1f}%")
        st.metric("Avg Memory Usage", f"{avg_mem_pct:.1f}%")
        st.metric("Metrics Collected", metrics_collected)
    
    # Detailed consolidation stats
    if 'consolidation_statistics' in kpis:
        st.markdown("---")
        st.markdown("### 🔄 Consolidation Statistics")
        
        cons_stats = kpis['consolidation_statistics']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Consolidations",
                cons_stats.get('total_consolidations', 0)
            )
        
        with col2:
            st.metric(
                "Total Migrations",
                cons_stats.get('total_migrations', 0)
            )
        
        with col3:
            st.metric(
                "Avg Saved per Cycle",
                f"{cons_stats.get('average_energy_saved_per_consolidation', 0):.2f} W"
            )


def render_migration_events(df: pd.DataFrame):
    """Render migration events timeline."""
    st.markdown("## 🔄 Migration Events")
    
    # Note: Real migration events would come from framework logs
    # This is a placeholder visualization
    
    st.info("""
    **Migration Event Tracking**
    
    Real-time migration events will be displayed here when the framework performs
    container consolidations. Each event shows:
    - Container ID
    - Source host → Destination host
    - Timestamp
    - Reason for migration
    """)
    
    # Sample migration table
    if not df.empty:
        # Detect state changes as proxy for migrations
        state_changes = []
        
        for host_id in df['host_id'].unique():
            host_data = df[df['host_id'] == host_id].sort_values('datetime')
            state_diff = host_data['active_containers'].diff()
            
            for idx, row in host_data[state_diff != 0].iterrows():
                # Format timestamp to Sri Lanka timezone string
                timestamp_str = format_sri_lanka_time(row['datetime'], '%Y-%m-%d %H:%M:%S')
                state_changes.append({
                    'Timestamp (SLT)': timestamp_str,
                    'Host': row['host_id'],
                    'Event': 'Container Added' if state_diff[idx] > 0 else 'Container Removed',
                    'Container Count': row['active_containers']
                })
        
        if state_changes:
            st.dataframe(
                pd.DataFrame(state_changes).sort_values('Timestamp (SLT)', ascending=False).head(20),
                use_container_width=True
            )
        else:
            st.write("No migration events detected yet")


def export_to_excel_with_graphs(df: pd.DataFrame, output_path: str = "output/energy_metrics_report.xlsx"):
    """Export data to Excel with graphs using openpyxl and matplotlib."""
    try:
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows
        from openpyxl.drawing.image import Image
        import matplotlib.pyplot as plt
        import io
        
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Energy Metrics Data"
        
        # Write data to Excel
        if not df.empty:
            # Prepare data for export
            export_df = df.copy()
            if 'datetime' in export_df.columns:
                export_df['datetime'] = pd.to_datetime(export_df['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Write headers
            for r in dataframe_to_rows(export_df, index=False, header=True):
                ws.append(r)
        
        # Create summary sheet
        ws_summary = wb.create_sheet("Summary")
        ws_summary.append(["Metric", "Value"])
        if not df.empty:
            latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()] if 'host_id' in df.columns else df.iloc[-1:]
            ws_summary.append(["Total Power (W)", f"{latest['power_watts'].sum():.2f}"])
            ws_summary.append(["Avg CPU Utilization (%)", f"{latest['cpu_utilization'].mean() * 100:.2f}"])
            ws_summary.append(["Avg Memory Utilization (%)", f"{latest['memory_utilization'].mean() * 100:.2f}"])
            if 'latency_ms' in df.columns:
                ws_summary.append(["Avg Latency (ms)", f"{latest['latency_ms'].mean():.2f}"])
            if 'throughput_mbps' in df.columns:
                ws_summary.append(["Avg Throughput (Mbps)", f"{latest['throughput_mbps'].mean():.2f}"])
            ws_summary.append(["Total Containers", f"{latest['active_containers'].sum():.0f}"])
            ws_summary.append(["Active Hosts", f"{(latest['state'] == 'active').sum():.0f}"])
        
        # Save workbook
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        wb.save(output_path)
        
        return output_path
    except Exception as e:
        st.error(f"Error exporting to Excel: {e}")
        return None


def export_to_excel_simple(df: pd.DataFrame):
    """Export data to Excel using pandas ExcelWriter (simpler approach)."""
    try:
        output_path = "output/energy_metrics_report.xlsx"
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare data for export
        export_df = df.copy()
        if 'datetime' in export_df.columns:
            export_df['datetime'] = pd.to_datetime(export_df['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write main data
            export_df.to_excel(writer, sheet_name='Energy Metrics Data', index=False)
            
            # Create summary sheet
            if not df.empty:
                latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()] if 'host_id' in df.columns else df.iloc[-1:]
                summary_data = {
                    'Metric': [
                        'Total Power (W)',
                        'Avg CPU Utilization (%)',
                        'Avg Memory Utilization (%)',
                        'Avg Latency (ms)',
                        'Avg Throughput (Mbps)',
                        'Total Containers',
                        'Active Hosts'
                    ],
                    'Value': [
                        f"{latest['power_watts'].sum():.2f}",
                        f"{latest['cpu_utilization'].mean() * 100:.2f}",
                        f"{latest['memory_utilization'].mean() * 100:.2f}",
                        f"{latest['latency_ms'].mean():.2f}" if 'latency_ms' in df.columns else 'N/A',
                        f"{latest['throughput_mbps'].mean():.2f}" if 'throughput_mbps' in df.columns else 'N/A',
                        f"{latest['active_containers'].sum():.0f}",
                        f"{(latest['state'] == 'active').sum():.0f}"
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return output_path
    except Exception as e:
        st.error(f"Error exporting to Excel: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None


def render_performance_metrics(df: pd.DataFrame):
    """Render latency and throughput performance metrics."""
    st.markdown("## ⚡ Performance Metrics")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Check if latency and throughput columns exist
    if 'latency_ms' not in df.columns or 'throughput_mbps' not in df.columns:
        st.info("⚠️ Latency and Throughput metrics are being collected. Please wait for new data points.")
        return
    
    # Latest metrics
    latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()].reset_index(drop=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_latency = latest['latency_ms'].mean()
        st.metric(
            label="⏱️ Avg Latency",
            value=f"{avg_latency:.2f} ms",
            delta=f"{(avg_latency - df['latency_ms'].mean()):.2f} ms" if len(df) > len(latest) else None
        )
    
    with col2:
        avg_throughput = latest['throughput_mbps'].mean()
        st.metric(
            label="📡 Avg Throughput",
            value=f"{avg_throughput:.2f} Mbps",
            delta=f"{(avg_throughput - df['throughput_mbps'].mean()):.2f} Mbps" if len(df) > len(latest) else None
        )
    
    with col3:
        min_latency = latest['latency_ms'].min()
        st.metric(
            label="⚡ Min Latency",
            value=f"{min_latency:.2f} ms"
        )
    
    with col4:
        max_throughput = latest['throughput_mbps'].max()
        st.metric(
            label="🚀 Max Throughput",
            value=f"{max_throughput:.2f} Mbps"
        )
    
    # Latency and Throughput charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏱️ Latency Over Time")
        if not df.empty and 'latency_ms' in df.columns:
            fig = px.line(
                df,
                x='datetime',
                y='latency_ms',
                color='host_id',
                title='Latency Trend by Host',
                labels={'latency_ms': 'Latency (ms)', 'datetime': 'Time'},
                template='plotly_white'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📡 Throughput Over Time")
        if not df.empty and 'throughput_mbps' in df.columns:
            fig = px.line(
                df,
                x='datetime',
                y='throughput_mbps',
                color='host_id',
                title='Throughput Trend by Host',
                labels={'throughput_mbps': 'Throughput (Mbps)', 'datetime': 'Time'},
                template='plotly_white'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Combined performance metrics
    st.markdown("### 📊 Performance Overview")
    if not df.empty and 'latency_ms' in df.columns and 'throughput_mbps' in df.columns:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Latency Distribution', 'Throughput Distribution'),
            vertical_spacing=0.15
        )
        
        # Latency distribution
        fig.add_trace(
            go.Histogram(
                x=latest['latency_ms'],
                name='Latency',
                marker_color='#e74c3c'
            ),
            row=1, col=1
        )
        
        # Throughput distribution
        fig.add_trace(
            go.Histogram(
                x=latest['throughput_mbps'],
                name='Throughput',
                marker_color='#2ecc71'
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Latency (ms)", row=1, col=1)
        fig.update_xaxes(title_text="Throughput (Mbps)", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        
        fig.update_layout(
            height=600,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_footer():
    """Render dashboard footer."""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Energy-Efficient Container Consolidation Framework</strong></p>
        <p>Developed by <strong>Ananthakumar Vithurshanan</strong> • 2025</p>
        <p>🌱 Sustainable Computing for Cloud Infrastructure</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main dashboard application."""
    # Initialize session state
    if 'export_excel' not in st.session_state:
        st.session_state['export_excel'] = False
    
    # Initialize data loader
    data_loader = DashboardDataLoader()
    
    # Render header
    render_header()
    
    # Render sidebar and get settings
    auto_refresh, refresh_interval = render_sidebar(data_loader)
    
    # Load data - always check for file changes
    # Get current file modification time to force reload if changed
    force_reload = False
    if data_loader.csv_path.exists():
        current_file_mtime = os.path.getmtime(data_loader.csv_path)
        last_known_mtime = st.session_state.get('file_check_mtime', 0)
        
        # If file modification time changed, force reload
        if current_file_mtime != last_known_mtime:
            force_reload = True
            st.session_state['file_check_mtime'] = current_file_mtime
    
    # Also check if user manually requested refresh
    if st.session_state.get('force_reload', False):
        force_reload = True
        st.session_state['force_reload'] = False
    
    df = data_loader.load_csv_data(force_reload=force_reload)
    kpis = data_loader.load_kpis()
    
    # Debug: Show what data we're actually loading
    if not df.empty:
        st.sidebar.markdown("### 🔍 Debug Info")
        st.sidebar.write(f"**Data Points:** {len(df)}")
        latest_dt_debug = df['datetime'].iloc[-1]
        latest_time_debug_str = format_sri_lanka_time(latest_dt_debug, '%Y-%m-%d %H:%M:%S')
        st.sidebar.write(f"**Latest Time:** {latest_time_debug_str} (SLT)")
        st.sidebar.write(f"**Total Power:** {df['power_watts'].sum():.0f}W")
        st.sidebar.write(f"**Hosts:** {df['host_id'].nunique()}")
        st.sidebar.write(f"**Containers:** {df['active_containers'].sum()}")
        st.sidebar.markdown("---")
    
    # Start main content with sticky header spacing
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Add JavaScript real-time clock (Sri Lanka timezone - UTC+5:30)
    st.markdown("""
    <script>
        function updateClock() {
            const now = new Date();
            // Sri Lanka timezone is UTC+5:30
            const sriLankaOffset = 5.5 * 60 * 60 * 1000; // 5.5 hours in milliseconds
            const utcTime = now.getTime() + (now.getTimezoneOffset() * 60 * 1000);
            const sriLankaTime = new Date(utcTime + sriLankaOffset);
            
            const timeString = sriLankaTime.toLocaleString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }) + ' (SLT)';
            
            // Update all clock elements
            const clockElements = document.querySelectorAll('.live-clock');
            clockElements.forEach(element => {
                element.textContent = timeString;
            });
        }
        
        // Update clock every second
        setInterval(updateClock, 1000);
        updateClock(); // Initial call
    </script>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tabs = st.tabs([
        "📊 Overview",
        "🖥️ Hosts",
        "💡 Energy",
        "📦 Containers",
        "📈 Utilization",
        "⚡ Performance",
        "🔄 Migrations",
        "🎯 KPIs"
    ])
    
    with tabs[0]:
        render_metrics_overview(df, kpis)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            # Quick energy chart
            if not df.empty:
                power_by_time = df.groupby('datetime')['power_watts'].sum().reset_index()
                fig = px.line(
                    power_by_time,
                    x='datetime',
                    y='power_watts',
                    title='Power Consumption Timeline',
                    template='plotly_white'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Quick host status
            if not df.empty:
                latest = df.loc[df.groupby('host_id')['timestamp'].idxmax()].reset_index()
                status_counts = latest['state'].value_counts().reset_index()
                status_counts.columns = ['State', 'Count']
                
                fig = px.pie(
                    status_counts,
                    values='Count',
                    names='State',
                    title='Host Status Distribution',
                    color='State',
                    color_discrete_map={'active': '#2ecc71', 'shutdown': '#f39c12', 'idle': '#f39c12'},  # Green for active, Orange/Yellow for shutdown/idle
                    template='plotly_white'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        render_host_overview(df)
    
    with tabs[2]:
        render_energy_consumption(df)
    
    with tabs[3]:
        render_container_distribution(df)
    
    with tabs[4]:
        render_utilization_trends(df)
    
    with tabs[5]:
        render_performance_metrics(df)
    
    with tabs[6]:
        render_migration_events(df)
    
    with tabs[7]:
        render_kpi_summary(kpis, df)
    
    # Handle Excel export
    if st.session_state.get('export_excel', False):
        if not df.empty:
            output_path = export_to_excel_simple(df)
            if output_path:
                st.success(f"✅ Data exported to Excel: {output_path}")
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=f.read(),
                        file_name="energy_metrics_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.warning("⚠️ No data available to export")
        st.session_state['export_excel'] = False
    
    # Close main content wrapper
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    render_footer()
    
    # Auto-refresh logic - enhanced for frequent automatic updates
    if auto_refresh:
        # Store refresh settings in session state for persistence
        st.session_state['auto_refresh'] = True
        st.session_state['refresh_interval'] = refresh_interval
        
        # Use JavaScript meta-refresh combined with Streamlit rerun for seamless updates
        # This ensures the page updates automatically without user interaction
        st.markdown(f"""
        <script>
            // Auto-refresh mechanism - updates every {refresh_interval} seconds
            let refreshInterval = {refresh_interval * 1000};
            let countdown = {refresh_interval};
            let refreshCount = 0;
            
            // Create or update countdown display
            function updateCountdown() {{
                // Find or create countdown element
                let countdownEl = document.getElementById('refresh-countdown');
                if (!countdownEl) {{
                    countdownEl = document.createElement('div');
                    countdownEl.id = 'refresh-countdown';
                    countdownEl.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: rgba(46, 204, 113, 0.9); color: white; padding: 10px 15px; border-radius: 5px; font-family: monospace; font-weight: bold; z-index: 9999; box-shadow: 0 2px 10px rgba(0,0,0,0.3);';
                    document.body.appendChild(countdownEl);
                }}
                countdownEl.innerHTML = `🔄 Next update in: ${{countdown}}s`;
            }}
            
            // Start countdown timer
            function startCountdown() {{
                countdown = {refresh_interval};
                updateCountdown();
                
                let countdownInterval = setInterval(function() {{
                    countdown--;
                    updateCountdown();
                    
                    if (countdown <= 0) {{
                        clearInterval(countdownInterval);
                        refreshCount++;
                        
                        // Use Streamlit's rerun API if available, otherwise reload page
                        if (window.parent !== undefined && window.parent.postMessage) {{
                            window.parent.postMessage({{
                                type: 'streamlit:rerun',
                                always: true
                            }}, '*');
                        }} else if (window.streamlit !== undefined && window.streamlit.rerun) {{
                            window.streamlit.rerun();
                        }} else {{
                            // Fallback to page reload
                            window.location.reload(true);
                        }}
                    }}
                }}, 1000);
            }}
            
            // Start the countdown immediately
            startCountdown();
            
            // Show refresh indicator in console (for debugging)
            console.log(`🔄 Auto-refresh enabled: every ${{refreshInterval/1000}}s`);
        </script>
        
        <!-- Meta refresh as backup (works even if JavaScript fails) -->
        <meta http-equiv="refresh" content="{refresh_interval};url=javascript:location.reload(true)">
        """, unsafe_allow_html=True)
        
        # Also use Streamlit's built-in mechanism
        # Check if file changed and trigger immediate rerun if needed
        if data_loader.csv_path.exists():
            current_mtime = os.path.getmtime(data_loader.csv_path)
            last_check_mtime = st.session_state.get('check_mtime', 0)
            
            # If file changed since last check, show notification
            if current_mtime != last_check_mtime:
                st.session_state['check_mtime'] = current_mtime
                # File changed - data will be reloaded on next rerun
                if current_mtime > last_check_mtime:
                    # Show visual indicator that data was updated
                    update_time = datetime.fromtimestamp(current_mtime, tz=timezone.utc)
                    update_time_str = format_sri_lanka_time(update_time, '%H:%M:%S')
                    st.sidebar.success(f"🔄 Data updated at {update_time_str} (SLT)")
    else:
        # Disable auto-refresh
        st.session_state['auto_refresh'] = False


if __name__ == "__main__":
    main()

