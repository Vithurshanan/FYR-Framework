"""
Helper Functions - Utility Layer
Common utility functions for the framework
"""

import random
import string
from datetime import datetime

def generate_workload_id(prefix: str = "workload") -> str:
    """Generate a unique workload ID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{prefix}_{timestamp}_{random_suffix}"

def calculate_power_consumption(cpu_util: float, p_idle: float, p_max: float) -> float:
    """Calculate power consumption based on CPU utilization."""
    return p_idle + (p_max - p_idle) * cpu_util

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_watts(watts: float) -> str:
    """Format watts to human readable format."""
    if watts < 1000:
        return f"{watts:.1f} W"
    else:
        return f"{watts/1000:.2f} kW"
