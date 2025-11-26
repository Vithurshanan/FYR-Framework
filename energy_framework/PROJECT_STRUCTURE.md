# Energy-Efficient Container Consolidation Framework
## Project Structure

```
energy_framework/
├── src/                           # Source code
│   ├── infrastructure/            # Infrastructure Layer
│   │   ├── __init__.py
│   │   └── host_monitor.py       # Host monitoring and metrics collection (CPU, Power, Memory)
│   ├── virtualization/           # Virtualization Layer
│   │   ├── __init__.py
│   │   └── docker_manager.py     # Docker Container management
│   ├── core/                     # Core Component Layer
│   │   ├── __init__.py
│   │   └── consolidation_engine.py # VM/Container modules, Dynamic resource pooling, Scheduling, Multi-tier consolidation
│   ├── orchestration/            # Workload Orchestration Layer
│   │   ├── __init__.py
│   │   └── energy_aware_scheduler.py # Load balancing, Energy scheduling
│   ├── sustainability/           # Sustainability Management Layer
│   │   ├── __init__.py
│   │   └── energy_metrics_manager.py # Carbon tracking, Energy monitoring
│   └── utils/                    # Utilities
│       ├── __init__.py
│       └── helpers.py            # Helper functions
├── dashboard/                    # Real-time Dashboard
│   └── dashboard.py              # Streamlit dashboard application with Excel export
├── output/                       # Generated Output
│   ├── reports/                  # Analysis reports (KPIs, Excel reports)
│   ├── energy_log.csv           # Energy metrics data (CPU, Memory, Latency, Throughput)
│   └── energy_log.json          # JSON format energy metrics
├── main.py                       # Main simulation runner
├── continuous_monitor.py         # Real-time monitoring system
├── start_realtime.py             # One-click startup script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── PROJECT_STRUCTURE.md          # This file
├── ARCHITECTURE.md               # Multi-layer architecture documentation
└── RESEARCH_QUESTIONS_OBJECTIVES.md # Research questions and objectives
```

## Multi-Layer Architecture

### 1. Sustainability Management Layer (`src/sustainability/`)
**Purpose:** Carbon tracking, Energy monitoring, Environmental impact assessment

**Components:**
- **EnergyMetricsManager**: Logs metrics, generates visualizations, and evaluates KPIs
- **Carbon Tracking**: Calculates CO₂ emissions based on power consumption
- **Energy Monitoring**: Real-time energy usage monitoring and reporting
- **Cost Estimation**: Estimates energy costs and operational expenses

**Key Features:**
- Real-time energy consumption tracking
- Carbon footprint calculation
- Environmental impact assessment
- Cost estimation and reporting
- KPI generation and analysis

### 2. Workload Orchestration Layer (`src/orchestration/`)
**Purpose:** Load balancing, Energy scheduling, Workload placement

**Components:**
- **EnergyAwareScheduler**: Intelligent workload placement based on energy efficiency
- **Load Balancing**: Distributes workloads across hosts for optimal resource utilization
- **Energy Scheduling**: Schedules workloads to minimize energy consumption
- **Workload Placement**: Places containers on the most energy-efficient hosts

**Key Features:**
- Energy-aware scheduling algorithms
- Load balancing with energy considerations
- Workload placement optimization
- SLA-aware scheduling
- Dynamic resource allocation

### 3. Core Component Layer (`src/core/`)
**Purpose:** VM/Container modules, Dynamic resource pooling, Scheduling, Multi-tier consolidation

**Components:**
- **ConsolidationEngine**: Implements energy-efficient consolidation algorithms
- **VM/Container Modules**: Manages virtual machines and containers
- **Dynamic Resource Pooling**: Dynamically pools and allocates resources
- **Multi-Tier Consolidation**: Consolidates workloads across multiple tiers

**Key Features:**
- Container consolidation algorithms
- Idle host detection and shutdown
- Dynamic resource pooling
- Multi-tier consolidation strategies
- Migration planning and execution

### 4. Virtualization Layer (`src/virtualization/`)
**Purpose:** Docker Container management, VM management

**Components:**
- **DockerManager**: Handles Docker container lifecycle management
- **Container Management**: Creates, starts, stops, and removes containers
- **VM Management**: Manages virtual machine instances
- **Container Migration**: Handles container migration between hosts

**Key Features:**
- Docker container management
- Container lifecycle operations
- VM management
- Container migration support
- Resource isolation

### 5. Infrastructure Layer (`src/infrastructure/`)
**Purpose:** CPU usage, Power usage, Memory usage, Network resources

**Components:**
- **HostMonitor**: Collects real-time host metrics (CPU, memory, power, temperature, latency, throughput)
- **HostCluster**: Manages multiple hosts and their states
- **Resource Monitoring**: Monitors CPU, memory, power, and network usage
- **Performance Metrics**: Tracks latency and throughput

**Key Features:**
- Real-time host monitoring
- CPU and memory utilization tracking
- Power consumption monitoring
- Temperature monitoring
- Latency and throughput measurement
- Host state management

## Key Metrics Collected

### Resource Metrics
- CPU Utilization (%)
- Memory Utilization (%)
- Power Consumption (Watts)
- Temperature (°C)
- Active Containers Count

### Performance Metrics
- **Latency (milliseconds)**: Response latency measurement
- **Throughput (Mbps)**: Network throughput measurement
- Response Time
- Network Bandwidth

### Energy Metrics
- Total Power Consumption (W)
- Energy per Container (W)
- Carbon Footprint (kg CO₂)
- Cost Estimation ($)

## Real-time Dashboard (`dashboard/`)

**Features:**
- Live host monitoring
- Energy consumption trends
- Container distribution
- **Performance metrics (Latency, Throughput)**
- Migration events
- Environmental impact metrics
- **Excel export functionality with graphs**

## Continuous Monitoring (`continuous_monitor.py`)

**Features:**
- Real-time data generation every 2 seconds
- Updates CSV/JSON files for dashboard consumption
- Collects CPU, memory, power, temperature, **latency, throughput** metrics
- Simulates host state changes and container migrations
- Provides live environmental impact metrics

## Data Export

### CSV Export
- **File:** `output/energy_log.csv`
- **Contains:** CPU, Memory, Power, Temperature, Containers, **Latency, Throughput**

### Excel Export
- **File:** `output/energy_metrics_report.xlsx`
- **Contains:** 
  - Energy Metrics Data (all metrics)
  - Summary sheet with KPIs
  - Graphs and visualizations

### JSON Export
- **File:** `output/energy_log.json`
- **Contains:** JSON format energy metrics
- **File:** `output/reports/kpis.json`
- **Contains:** Key Performance Indicators

## Usage

### Quick Start
```bash
# Start continuous real-time monitoring
python continuous_monitor.py

# Start dashboard (in another terminal)
streamlit run dashboard/dashboard.py --server.port 8501

# Run simulation
python main.py
```

### Real-time Monitoring
- **URL**: http://localhost:8501
- **Auto-refresh**: Every 2 seconds
- **Features**: Live energy consumption, host status, container distribution, environmental impact

## Features

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
