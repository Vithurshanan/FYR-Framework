#!/usr/bin/env python3
"""
Start Real-Time Energy Monitoring System
Launches both the continuous monitor and dashboard
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_continuous_monitor():
    """Start the continuous energy monitor."""
    print("🚀 Starting Continuous Energy Monitor...")
    return subprocess.Popen([sys.executable, "continuous_monitor.py"])

def start_dashboard():
    """Start the Streamlit dashboard."""
    print("📊 Starting Streamlit Dashboard...")
    return subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", 
        "dashboard/dashboard.py", 
        "--server.port", "8501",
        "--server.runOnSave", "true"
    ])

def main():
    """Main startup function."""
    print("=" * 60)
    print("🌱 ENERGY-EFFICIENT CONTAINER CONSOLIDATION FRAMEWORK")
    print("📊 Real-Time Monitoring System")
    print("=" * 60)
    
    # Check if required files exist
    required_files = [
        "continuous_monitor.py",
        "dashboard/dashboard.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file not found: {file}")
            sys.exit(1)
    
    print("✅ All required files found")
    print()
    
    try:
        # Start continuous monitor
        monitor_process = start_continuous_monitor()
        time.sleep(2)  # Give monitor time to start
        
        # Start dashboard
        dashboard_process = start_dashboard()
        time.sleep(3)  # Give dashboard time to start
        
        print()
        print("🎉 REAL-TIME MONITORING SYSTEM LAUNCHED!")
        print()
        print("📊 Dashboard URL: http://localhost:8501")
        print("🔄 Continuous Monitor: Running in background")
        print("📈 Data Updates: Every 2 seconds")
        print()
        print("⏹️  Press Ctrl+C to stop all services")
        print("=" * 60)
        
        # Wait for user interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)
    
    finally:
        # Clean up processes
        try:
            if 'monitor_process' in locals():
                monitor_process.terminate()
            if 'dashboard_process' in locals():
                dashboard_process.terminate()
            print("✅ Services stopped successfully")
        except:
            pass

if __name__ == "__main__":
    main()
