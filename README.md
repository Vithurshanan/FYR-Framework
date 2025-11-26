<div align="center">

# 🌱 FYR: Energy-Efficient Container Consolidation Framework

**Real-time energy, cost, and carbon monitoring for containerized cloud workloads.**

[![Status](https://img.shields.io/badge/status-active-success)](https://github.com/Vithurshanan/FYR-Framework)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

## 💡 What is FYR?

FYR is a **research-grade framework** for exploring and prototyping **energy-efficient container consolidation** and **sustainable cloud infrastructure** strategies.

- **Real-time energy monitoring** for hosts and containers  
- **Container consolidation algorithms** to reduce idle capacity  
- **Sustainability analytics** (carbon, cost, and efficiency)  
- **Interactive dashboard** for visualizing system behavior over time  

Use it to **experiment, teach, or prototype** green cloud strategies in a fully reproducible environment.

---

## 🌍 Why This Framework? (Problem & Objectives)

Modern data centres suffer from:
- **High energy consumption** and electricity costs  
- **Poor resource utilisation** with many **idle or underutilised hosts**  
- **Unnecessary carbon emissions** from wasted power  

FYR is designed to:
1. **Consolidate containers** onto fewer, better-utilised hosts  
2. **Shut down idle hosts** safely to save energy  
3. **Schedule workloads energy‑aware**, respecting SLAs (Gold/Silver/Bronze)  
4. **Continuously monitor** energy, performance, and environmental impact  

These high-level goals are explained in more depth in `FRAMEWORK_EXPLANATION.md`, while this README provides the practical overview.

---

## 🚀 Quick Start

> From the `energy_framework/` directory:

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. One-command real-time system (recommended)

```bash
python start_realtime.py
```

This will start:
- ✅ Continuous monitoring & data generation (every 2 seconds)
- ✅ Streamlit dashboard at `http://localhost:8501`
- ✅ Live sustainability metrics and charts

### 3. Manual control (advanced)

```bash
# Terminal 1: Continuous monitoring & data generation
python continuous_monitor.py

# Terminal 2: Dashboard
streamlit run dashboard/dashboard.py --server.port 8501

# Terminal 3: Run consolidation / scheduling simulation (optional)
python main.py
```

---

## 📊 Real-Time Dashboard

**URL**: `http://localhost:8501`

The dashboard is built for **live operations**:

- 🟢 **Live Status** – host health, utilization, and container distribution  
- 📈 **Dynamic Charts** – power, energy, and efficiency metrics over time  
- 📦 **Container View** – placement, migrations, and consolidation effects  
- 🌍 **Environmental Metrics** – CO₂ emissions and cost estimation  
- 🔄 **Auto-Refresh** – updates every ~2 seconds for an operational feel  

---

## 🏗️ Architecture Overview

FYR follows a **clean, layered architecture** to keep research logic modular and extensible.

### Project Structure

```text
energy_framework/
├── src/                      # Core framework logic
│   ├── infrastructure/       # Host monitoring & raw metrics
│   ├── virtualization/       # Container & VM abstraction
│   ├── core/                 # Consolidation & optimization engine
│   ├── orchestration/        # Energy-aware scheduling policies
│   ├── sustainability/       # CO₂, cost, and efficiency models
│   └── utils/                # Shared helpers/utilities
├── dashboard/                # Streamlit-based real-time dashboard
├── output/                   # Generated traces, logs, and reports
├── continuous_monitor.py     # Real-time data generator
├── start_realtime.py         # One-click end-to-end launcher
├── main.py                   # Simulation entrypoint
└── requirements.txt          # Python dependencies
```

### Core Layers (5-Layer Design)

- **Infrastructure Layer** – host monitoring, metrics collection, host states  
- **Virtualization Layer** – Docker/container lifecycle and migrations  
- **Core Component Layer** – consolidation algorithms and migration planning  
- **Workload Orchestration Layer** – energy-aware, SLA-aware scheduling and load balancing  
- **Sustainability Management Layer** – energy, carbon, cost, and KPI tracking  
- **Dashboard** – real-time visualization and reporting on top of these layers  

---

## 📈 Real-Time Monitoring & Data

The monitoring subsystem:

- Generates **realistic, high-frequency** time-series data (every 2 seconds)  
- Records host and container states for later **analysis and replay**  
- Feeds the dashboard with **live CSV/JSON updates**  
- Captures the impact of **consolidation and scheduling decisions**  

This makes FYR ideal for:

- Comparing different consolidation algorithms  
- Demonstrating energy impact in lectures or workshops  
- Building datasets for further analysis or ML-based scheduling  

### Key Metrics Collected

- **Resource metrics** – CPU %, memory %, power (W), temperature, containers/host  
- **Performance metrics** – latency (ms), throughput (Mbps), response times  
- **Energy metrics** – total/average power, total energy (Wh), power per container  
- **Sustainability metrics** – carbon footprint (kg CO₂), estimated energy cost, efficiency score  
- **Fleet metrics** – active/idle/shutdown hosts, container distribution and migrations  

---

## 🌱 Sustainability & Metrics

FYR focuses on **making sustainability visible and measurable**:

- 🌍 **Carbon Footprint** – CO₂ emissions derived from energy usage  
- 💰 **Cost Estimation** – approximate energy cost per time unit  
- ⚙️ **Efficiency Score** – how much energy is saved vs. baseline  
- 🔋 **Resource Utilization** – CPU/memory usage and consolidation gains  

These metrics update in **real time** and are available both:
- In the **dashboard**, and  
- In the **output data** for offline analysis.  

---

## 🎯 Feature Highlights

### ✅ Real-Time Operations
- Continuous monitoring loop with configurable interval  
- Live system state in the dashboard  
- Auto-refreshing, time-series visualizations  

### ✅ Energy & Consolidation Logic
- Container consolidation strategies (extendable and pluggable)  
- Idle host detection and potential shutdown/parking logic  
- Hooks for trying out **new scheduling / consolidation policies**  

### ✅ Research & Teaching Friendly
- Clean separation of concerns for experimentation  
- Easy to plug in custom algorithms in `core/` and `orchestration/`  
- Ready-to-use visual front-end for demos and presentations  

### 🎓 Research Focus (From the Full Framework Explanation)

FYR is built around concrete **research questions**, including:
- **RQ1 – Energy efficiency**: How much energy can consolidation save while maintaining SLAs?  
- **RQ2 – Resource utilisation**: What is the optimal utilisation vs. energy trade-off?  
- **RQ3 – Performance impact**: How do consolidation strategies affect latency and throughput?  
- **RQ4 – Environmental impact**: What carbon and cost reductions are achievable?  
- **RQ5 – Scalability**: How does the framework behave for different cluster sizes and workloads?  

Corresponding **objectives** include designing the multi-layer framework, building the monitoring and sustainability stack, and running experiments to quantify energy savings and performance effects.

---

## ✅ Benefits & Results (High-Level Summary)

Experiments described in `FRAMEWORK_EXPLANATION.md` highlight that FYR can:
- Achieve **~20–30% energy reduction** through consolidation and idle host shutdown  
- **Maintain SLA compliance**, low latency, and acceptable throughput  
- Provide **full observability** of hosts, containers, energy, and carbon in real-time  
- Generate **reports and exports** (CSV/JSON/Excel) suitable for academic analysis or industry reporting  

---

## 🛠️ Extending FYR

### Add a new algorithm or policy

1. Implement your logic in the relevant `src/` submodule:  
   - `core/` for consolidation / optimization algorithms  
   - `orchestration/` for scheduling and decision policies  
2. Wire it into the execution flow in `main.py` or `continuous_monitor.py`.  
3. Expose its outputs to the dashboard via the existing data pipeline.  
4. Add or update charts in `dashboard/dashboard.py` to visualize the new behavior.  

### Typical development workflow

```bash
# Run a simulation-only experiment
python main.py

# Observe live monitoring behavior
python continuous_monitor.py

# Launch the dashboard (if not using start_realtime.py)
streamlit run dashboard/dashboard.py --server.port 8501
```

---

## 🤝 Contributing

Contributions, ideas, and issue reports are very welcome.

- Suggest new **energy models** or **sustainability metrics**  
- Add or compare **consolidation algorithms**  
- Improve the **dashboard UX** or visualizations  

Feel free to open an **issue** or **pull request** on GitHub.

---

## 📚 Citation (Research Use)

If you use this framework for academic work, you can cite it informally as:

> V. Vithurshanan, *FYR: Energy-Efficient Container Consolidation Framework for Sustainable Cloud Computing*, 2025.  

(A formal BibTeX entry can be added once a paper/preprint is published.)

---

## 📝 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for full details.

---

**🌱 Built for Sustainable Computing · 📊 Real-Time Monitoring · ⚡ Experiment-Ready**
