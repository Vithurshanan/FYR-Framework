#!/usr/bin/env python3
"""
Continuous Real-Time Energy Monitor
Generates live energy monitoring data continuously for the dashboard
"""

import time
import random
import pandas as pd
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import threading
import signal
import sys

class ContinuousEnergyMonitor:
    """Continuous real-time energy monitoring system."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.csv_path = self.output_dir / "energy_log.csv"
        self.json_path = self.output_dir / "energy_log.json"
        self.kpis_path = self.output_dir / "reports" / "kpis.json"
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        
        # Host configurations
        self.hosts = [
            {"id": "host-001", "cores": 4, "ram_gb": 8.0, "p_idle": 45, "p_max": 120},
            {"id": "host-002", "cores": 8, "ram_gb": 16.0, "p_idle": 80, "p_max": 200},
            {"id": "host-003", "cores": 6, "ram_gb": 12.0, "p_idle": 60, "p_max": 150},
            {"id": "host-004", "cores": 4, "ram_gb": 8.0, "p_idle": 45, "p_max": 120},
            {"id": "host-005", "cores": 8, "ram_gb": 16.0, "p_idle": 80, "p_max": 200},
        ]
        
        self.running = True
        self.data_points = 0
        
        # Initialize CSV with headers if it doesn't exist
        if not self.csv_path.exists():
            self._initialize_csv()
    
    def _initialize_csv(self):
        """Initialize CSV file with headers."""
        headers = [
            'timestamp', 'datetime', 'host_id', 'cpu_utilization', 'memory_utilization',
            'cores', 'ram_gb', 'power_watts', 'temperature_c', 'active_containers',
            'state', 'is_idle', 'latency_ms', 'throughput_mbps'
        ]
        df = pd.DataFrame(columns=headers)
        df.to_csv(self.csv_path, index=False)
    
    def _calculate_power_consumption(self, cpu_util, p_idle, p_max):
        """Calculate power consumption based on CPU utilization."""
        return p_idle + (p_max - p_idle) * cpu_util
    
    def _generate_realistic_metrics(self, host):
        """Generate realistic metrics for a host."""
        # Simulate realistic CPU and memory patterns
        base_cpu = random.uniform(0.3, 0.8)
        cpu_variation = random.uniform(-0.1, 0.1)
        cpu_util = max(0.1, min(0.95, base_cpu + cpu_variation))
        
        base_memory = random.uniform(0.4, 0.7)
        memory_variation = random.uniform(-0.05, 0.05)
        memory_util = max(0.2, min(0.9, base_memory + memory_variation))
        
        # Calculate power consumption
        power = self._calculate_power_consumption(cpu_util, host["p_idle"], host["p_max"])
        
        # Generate realistic container count
        max_containers = host["cores"] * 2
        active_containers = random.randint(0, max_containers)
        
        # Determine host state
        if cpu_util < 0.1 and memory_util < 0.1:
            state = "idle"
            is_idle = True
        elif cpu_util > 0.9 or memory_util > 0.9:
            state = "overloaded"
            is_idle = False
        else:
            state = "active"
            is_idle = False
        
        # Generate temperature (correlates with CPU usage)
        temperature = 35 + (cpu_util * 25) + random.uniform(-2, 2)
        
        # Generate latency (lower is better, inversely related to CPU utilization)
        # Higher CPU utilization may lead to higher latency
        base_latency = 10.0  # Base latency in ms
        latency_variation = cpu_util * 50  # Latency increases with CPU usage
        latency_ms = base_latency + latency_variation + random.uniform(-5, 5)
        latency_ms = max(5.0, min(100.0, latency_ms))  # Clamp between 5-100ms
        
        # Generate throughput (higher is better, related to CPU and containers)
        # More containers and better CPU utilization = higher throughput
        base_throughput = 100.0  # Base throughput in Mbps
        throughput_factor = (cpu_util * 0.7 + memory_util * 0.3) * active_containers
        throughput_mbps = base_throughput + (throughput_factor * 50) + random.uniform(-10, 10)
        throughput_mbps = max(50.0, min(1000.0, throughput_mbps))  # Clamp between 50-1000 Mbps
        
        return {
            'cpu_utilization': cpu_util,
            'memory_utilization': memory_util,
            'power_watts': power,
            'temperature_c': temperature,
            'active_containers': active_containers,
            'state': state,
            'is_idle': is_idle,
            'latency_ms': latency_ms,
            'throughput_mbps': throughput_mbps
        }
    
    def _generate_data_point(self):
        """Generate a single data point for all hosts."""
        current_time = datetime.now(timezone.utc)
        timestamp = current_time.timestamp()
        datetime_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        data_points = []
        
        for host in self.hosts:
            metrics = self._generate_realistic_metrics(host)
            
            data_point = {
                'timestamp': timestamp,
                'datetime': datetime_str,
                'host_id': host["id"],
                'cpu_utilization': metrics['cpu_utilization'],
                'memory_utilization': metrics['memory_utilization'],
                'cores': host["cores"],
                'ram_gb': host["ram_gb"],
                'power_watts': metrics['power_watts'],
                'temperature_c': metrics['temperature_c'],
                'active_containers': metrics['active_containers'],
                'state': metrics['state'],
                'is_idle': metrics['is_idle'],
                'latency_ms': metrics['latency_ms'],
                'throughput_mbps': metrics['throughput_mbps']
            }
            data_points.append(data_point)
        
        return data_points
    
    def _update_csv(self, data_points):
        """Update CSV file with new data points."""
        try:
            # Read existing data
            if self.csv_path.exists() and os.path.getsize(self.csv_path) > 0:
                df = pd.read_csv(self.csv_path)
            else:
                df = pd.DataFrame()
            
            # Append new data
            new_df = pd.DataFrame(data_points)
            df = pd.concat([df, new_df], ignore_index=True)
            
            # Keep only last 1000 data points to prevent file from growing too large
            if len(df) > 1000:
                df = df.tail(1000).reset_index(drop=True)
            
            # Save to CSV
            df.to_csv(self.csv_path, index=False)
            
            # Also save as JSON for dashboard
            df.to_json(self.json_path, orient='records', date_format='iso')
            
            self.data_points += len(data_points)
            
        except Exception as e:
            print(f"Error updating CSV: {e}")
    
    def _update_kpis(self):
        """Update KPIs file."""
        try:
            if self.csv_path.exists() and os.path.getsize(self.csv_path) > 0:
                df = pd.read_csv(self.csv_path)
                
                if not df.empty:
                    latest = df.groupby('host_id').last()
                    
                    # Calculate all KPIs
                    total_power = float(latest['power_watts'].sum())
                    avg_power = float(latest['power_watts'].mean())
                    total_containers = int(latest['active_containers'].sum())
                    total_hosts = int(len(latest))
                    active_hosts = int((latest['state'] == 'active').sum())
                    idle_hosts = int((latest['state'] == 'idle').sum())
                    
                    # Calculate derived metrics
                    power_per_container = (avg_power / total_containers) if total_containers > 0 else 0.0
                    containers_per_host = (total_containers / total_hosts) if total_hosts > 0 else 0.0
                    
                    # Calculate total energy (approximate: average power * time in hours)
                    # For real-time monitoring, estimate based on average power
                    # Assuming 1 hour of operation for estimation
                    total_energy_wh = avg_power * 1.0  # Watts * hours = Wh
                    
                    kpis = {
                        'total_power_watts': total_power,
                        'average_power_watts': avg_power,
                        'total_energy_wh': total_energy_wh,
                        'average_power_per_container': power_per_container,
                        'total_containers': total_containers,
                        'total_hosts': total_hosts,
                        'active_hosts': active_hosts,
                        'average_active_hosts': float(active_hosts),  # For compatibility
                        'idle_hosts': idle_hosts,
                        'average_containers_per_host': containers_per_host,
                        'average_cpu_utilization': float(latest['cpu_utilization'].mean() * 100),  # Already in percentage
                        'average_memory_utilization': float(latest['memory_utilization'].mean() * 100),  # Already in percentage
                        'total_data_points': int(len(df)),
                        'metrics_collected': int(len(df)),  # Alias for compatibility
                        'last_updated': datetime.now().isoformat(),
                        'carbon_footprint_kg': float((total_power * 0.0005) / 1000),
                        'estimated_cost_usd': float((total_power * 0.12) / 1000)
                    }
                    
                    with open(self.kpis_path, 'w') as f:
                        json.dump(kpis, f, indent=2)
                        
        except Exception as e:
            print(f"Error updating KPIs: {e}")
    
    def start_monitoring(self, interval: float = 2.0):
        """Start continuous monitoring."""
        print(f"🚀 Starting Continuous Real-Time Energy Monitor")
        print(f"📊 Generating data every {interval} seconds")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🌐 Dashboard URL: http://localhost:8501")
        print(f"⏹️  Press Ctrl+C to stop")
        print("-" * 60)
        
        try:
            while self.running:
                # Generate new data point
                data_points = self._generate_data_point()
                
                # Update files
                self._update_csv(data_points)
                self._update_kpis()
                
                # Print status
                current_time = datetime.now().strftime("%H:%M:%S")
                total_power = sum(dp['power_watts'] for dp in data_points)
                active_hosts = sum(1 for dp in data_points if dp['state'] == 'active')
                total_containers = sum(dp['active_containers'] for dp in data_points)
                
                print(f"[{current_time}] Power: {total_power:.0f}W | Hosts: {active_hosts}/5 | Containers: {total_containers} | Data Points: {self.data_points}")
                
                # Wait for next update
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Error in monitoring: {e}")
        finally:
            self.running = False
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.running = False


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print("\n🛑 Received interrupt signal. Stopping monitor...")
    sys.exit(0)


if __name__ == "__main__":
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start monitor
    monitor = ContinuousEnergyMonitor()
    monitor.start_monitoring(interval=2.0)  # Update every 2 seconds
