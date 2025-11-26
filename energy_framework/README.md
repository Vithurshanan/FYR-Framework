# 🌱 Energy-Efficient Container Consolidation Framework

A comprehensive, real-time monitoring and optimization system for sustainable cloud infrastructure deployment.

## 🚀 Quick Start

### Real-Time Monitoring (Recommended)
```bash
# Start the complete real-time monitoring system
python start_realtime.py
```
This will launch:
- Continuous energy monitor (generates live data every 2 seconds)
- Streamlit dashboard (http://localhost:8501)

### Manual Start
```bash
# Terminal 1: Start continuous monitoring
python continuous_monitor.py

# Terminal 2: Start dashboard
streamlit run dashboard/dashboard.py --server.port 8501

# Terminal 3: Run simulation (optional)
python main.py
```

## 📊 Real-Time Dashboard

**URL**: http://localhost:8501

### Features
- 🟢 **Live Status**: Real-time system monitoring
- 📈 **Dynamic Charts**: Auto-updating energy consumption graphs
- 🖥️ **Host Overview**: Live host status and resource utilization
- 📦 **Container Tracking**: Real-time container distribution
- 🌱 **Environmental Impact**: Carbon footprint and cost estimation
- 🔄 **Auto-Refresh**: Updates every 2 seconds

## 🏗️ Clean Architecture

### Project Structure
```
energy_framework/
├── src/                    # Clean source code
│   ├── infrastructure/     # Host monitoring
│   ├── virtualization/     # Container management
│   ├── core/              # Consolidation algorithms
│   ├── orchestration/     # Energy-aware scheduling
│   ├── sustainability/    # Environmental tracking
│   └── utils/             # Helper functions
├── dashboard/             # Real-time dashboard
├── output/               # Generated data and reports
├── continuous_monitor.py # Real-time data generator
├── start_realtime.py     # One-click startup
├── main.py              # Simulation runner
└── requirements.txt     # Dependencies
```

### Core Components
- **Infrastructure Layer**: Host monitoring and metrics collection
- **Virtualization Layer**: Container lifecycle management
- **Core Engine**: Energy-efficient consolidation algorithms
- **Orchestration**: Energy-aware workload scheduling
- **Sustainability**: Environmental impact tracking
- **Dashboard**: Real-time visualization and monitoring

## 🔧 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start real-time monitoring
python start_realtime.py
```

## 📈 Real-Time Monitoring

The framework includes a **continuous monitoring system** that:

- Generates realistic energy consumption data every 2 seconds
- Updates CSV/JSON files for dashboard consumption
- Simulates host state changes and container migrations
- Provides live environmental impact metrics
- Maintains data history for trend analysis

## 🌱 Environmental Impact

Track sustainability metrics in real-time:
- **Carbon Footprint**: CO₂ emissions calculation
- **Cost Estimation**: Energy cost per hour
- **Efficiency Score**: Energy optimization percentage
- **Resource Utilization**: CPU/Memory efficiency

## 🎯 Key Features

### ✅ Real-time Monitoring
- Live energy consumption tracking
- Dynamic host status updates
- Real-time container distribution
- Environmental impact metrics

### ✅ Energy Efficiency
- Container consolidation algorithms
- Idle host detection and shutdown
- Power-aware workload scheduling
- Energy savings optimization

### ✅ Sustainability Tracking
- Carbon footprint calculation
- Cost estimation
- Efficiency score computation
- Environmental impact reporting

### ✅ Professional Dashboard
- Sticky header navigation
- Interactive charts and graphs
- Real-time status indicators
- Responsive design

## 🛠️ Development

### Adding New Features
1. Create modules in appropriate `src/` subdirectories
2. Update imports in `main.py` and `continuous_monitor.py`
3. Add dashboard visualizations in `dashboard/dashboard.py`
4. Update documentation

### Testing
```bash
# Run simulation
python main.py

# Test real-time monitoring
python continuous_monitor.py

# Start dashboard
streamlit run dashboard/dashboard.py --server.port 8501
```

## 📝 License

MIT License - See LICENSE file for details.

---

**🌱 Built for Sustainable Computing | 📊 Real-Time Monitoring | 🚀 Production Ready**