"""
Host Monitor - Infrastructure Layer
Simplified version for real-time monitoring
"""

import time
import random
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class HostMetrics:
    """Host metrics data structure."""
    timestamp: float
    host_id: str
    cpu_utilization: float
    memory_utilization: float
    power_watts: float
    temperature_c: float
    active_containers: int
    state: str
    is_idle: bool
    latency_ms: float  # Response latency in milliseconds
    throughput_mbps: float  # Network throughput in Mbps

class HostMonitor:
    """Simplified host monitor for real-time monitoring."""
    
    def __init__(self, host_id: str, cores: int = 4, ram_gb: float = 8.0):
        self.host_id = host_id
        self.cores = cores
        self.ram_gb = ram_gb
        self.p_idle = 45.0
        self.p_max = 120.0
    
    def collect_metrics(self) -> HostMetrics:
        """Collect current host metrics."""
        timestamp = datetime.now(timezone.utc).timestamp()
        
        # Generate realistic metrics
        cpu_util = random.uniform(0.1, 0.9)
        memory_util = random.uniform(0.2, 0.8)
        power = self.p_idle + (self.p_max - self.p_idle) * cpu_util
        temperature = 35 + (cpu_util * 25) + random.uniform(-2, 2)
        containers = random.randint(0, self.cores * 2)
        
        # Generate latency (lower is better, inversely related to CPU utilization)
        # Higher CPU utilization may lead to higher latency
        base_latency = 10.0  # Base latency in ms
        latency_variation = cpu_util * 50  # Latency increases with CPU usage
        latency_ms = base_latency + latency_variation + random.uniform(-5, 5)
        latency_ms = max(5.0, min(100.0, latency_ms))  # Clamp between 5-100ms
        
        # Generate throughput (higher is better, related to CPU and containers)
        # More containers and better CPU utilization = higher throughput
        base_throughput = 100.0  # Base throughput in Mbps
        throughput_factor = (cpu_util * 0.7 + memory_util * 0.3) * containers
        throughput_mbps = base_throughput + (throughput_factor * 50) + random.uniform(-10, 10)
        throughput_mbps = max(50.0, min(1000.0, throughput_mbps))  # Clamp between 50-1000 Mbps
        
        # Determine state
        if cpu_util < 0.1 and memory_util < 0.1:
            state = "idle"
            is_idle = True
        elif cpu_util > 0.9 or memory_util > 0.9:
            state = "overloaded"
            is_idle = False
        else:
            state = "active"
            is_idle = False
        
        return HostMetrics(
            timestamp=timestamp,
            host_id=self.host_id,
            cpu_utilization=cpu_util,
            memory_utilization=memory_util,
            power_watts=power,
            temperature_c=temperature,
            active_containers=containers,
            state=state,
            is_idle=is_idle,
            latency_ms=latency_ms,
            throughput_mbps=throughput_mbps
        )

class HostCluster:
    """Simplified host cluster for real-time monitoring."""
    
    def __init__(self):
        self.hosts = []
    
    def add_host(self, host: HostMonitor):
        """Add a host to the cluster."""
        self.hosts.append(host)
    
    def get_all_metrics(self) -> List[HostMetrics]:
        """Get metrics from all hosts."""
        return [host.collect_metrics() for host in self.hosts]
