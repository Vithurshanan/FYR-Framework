"""
Main Execution Script - Energy-Efficient Container Consolidation Framework

Integrates all components and runs the complete simulation workflow.
"""

import os
import sys
import time
import logging
import random

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infrastructure.host_monitor import HostMonitor, HostCluster
from virtualization.docker_manager import DockerManager
from core.consolidation_engine import ConsolidationEngine
from orchestration.energy_aware_scheduler import EnergyAwareScheduler
from sustainability.energy_metrics_manager import EnergyMetricsManager
from utils.helpers import generate_workload_id


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('energy_framework.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print framework banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║   ENERGY-EFFICIENT CONTAINER CONSOLIDATION FRAMEWORK             ║
    ║   Sustainable Software Deployment for Cloud Environments         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def create_sample_hosts(num_hosts: int = 5) -> HostCluster:
    """
    Create a cluster of sample hosts.
    
    Args:
        num_hosts: Number of hosts to create
        
    Returns:
        HostCluster with initialized hosts
    """
    logger.info(f"Creating cluster with {num_hosts} hosts...")
    
    cluster = HostCluster()
    
    # Create diverse host configurations
    host_configs = [
        {'cpu_cores': 4, 'memory_gb': 8.0, 'p_idle': 50, 'p_max': 200},
        {'cpu_cores': 8, 'memory_gb': 16.0, 'p_idle': 80, 'p_max': 300},
        {'cpu_cores': 6, 'memory_gb': 12.0, 'p_idle': 60, 'p_max': 250},
        {'cpu_cores': 4, 'memory_gb': 8.0, 'p_idle': 45, 'p_max': 180},
        {'cpu_cores': 8, 'memory_gb': 16.0, 'p_idle': 85, 'p_max': 320},
    ]
    
    for i in range(num_hosts):
        config = host_configs[i % len(host_configs)]
        
        host_id = f"host-{i+1:03d}"
        monitor = HostMonitor(
            host_id=host_id,
            cpu_cores=config['cpu_cores'],
            memory_gb=config['memory_gb'],
            is_simulated=True,
            p_idle=config['p_idle'],
            p_max=config['p_max']
        )
        
        # Set initial simulated load (varied)
        initial_cpu = random.uniform(0.1, 0.3)
        initial_mem = random.uniform(0.2, 0.4)
        monitor.set_simulated_load(initial_cpu, initial_mem)
        
        cluster.add_host(monitor)
        
        logger.info(
            f"  Added {host_id}: {config['cpu_cores']} cores, "
            f"{config['memory_gb']}GB RAM"
        )
    
    return cluster


def create_sample_workloads() -> list:
    """
    Create sample workload specifications.
    
    Returns:
        List of workload dictionaries
    """
    workload_types = [
        # Web servers
        {'prefix': 'web', 'image': 'nginx:latest', 'cpu': (0.5, 1.5), 'mem': (0.5, 2.0), 'sla': 'gold'},
        # Databases
        {'prefix': 'db', 'image': 'postgres:latest', 'cpu': (1.0, 2.0), 'mem': (2.0, 4.0), 'sla': 'gold'},
        # API services
        {'prefix': 'api', 'image': 'python:3.10', 'cpu': (0.5, 1.0), 'mem': (1.0, 2.0), 'sla': 'silver'},
        # Background workers
        {'prefix': 'worker', 'image': 'python:3.10', 'cpu': (0.25, 0.75), 'mem': (0.5, 1.5), 'sla': 'bronze'},
        # Cache services
        {'prefix': 'cache', 'image': 'redis:latest', 'cpu': (0.5, 1.0), 'mem': (1.0, 2.0), 'sla': 'silver'},
    ]
    
    workloads = []
    
    # Create 15 diverse workloads
    for i in range(15):
        wtype = workload_types[i % len(workload_types)]
        
        cpu_request = round(random.uniform(*wtype['cpu']), 2)
        mem_request = round(random.uniform(*wtype['mem']), 2)
        
        workload = {
            'name': f"{wtype['prefix']}-{i+1:02d}",
            'image': wtype['image'],
            'cpu_request': cpu_request,
            'memory_request_gb': mem_request,
            'sla_tier': wtype['sla']
        }
        
        workloads.append(workload)
    
    logger.info(f"Created {len(workloads)} sample workloads")
    
    return workloads


def run_simulation(
    num_hosts: int = 5,
    num_cycles: int = 10,
    consolidation_interval: int = 3,
    use_real_docker: bool = False
):
    """
    Run complete simulation workflow.
    
    Args:
        num_hosts: Number of hosts in cluster
        num_cycles: Number of simulation cycles
        consolidation_interval: Run consolidation every N cycles
        use_real_docker: Whether to use real Docker API
    """
    print_banner()
    
    logger.info("=" * 70)
    logger.info("SIMULATION START")
    logger.info("=" * 70)
    logger.info(f"Configuration:")
    logger.info(f"  Hosts: {num_hosts}")
    logger.info(f"  Cycles: {num_cycles}")
    logger.info(f"  Consolidation Interval: {consolidation_interval}")
    logger.info(f"  Docker Mode: {'Real' if use_real_docker else 'Simulated'}")
    logger.info("=" * 70)
    
    # Initialize components
    logger.info("\n[1/7] Initializing host cluster...")
    host_cluster = create_sample_hosts(num_hosts)
    
    logger.info("\n[2/7] Initializing Docker manager...")
    docker_manager = DockerManager(use_real_docker=use_real_docker)
    
    logger.info("\n[3/7] Initializing consolidation engine...")
    consolidation_engine = ConsolidationEngine(
        host_cluster=host_cluster,
        docker_manager=docker_manager,
        consolidation_threshold=0.3,
        max_utilization=0.8
    )
    
    logger.info("\n[4/7] Initializing energy-aware scheduler...")
    scheduler = EnergyAwareScheduler(
        host_cluster=host_cluster,
        docker_manager=docker_manager,
        power_weight=0.4,
        utilization_weight=0.4,
        sla_weight=0.2
    )
    
    logger.info("\n[5/7] Initializing energy metrics manager...")
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    metrics_manager = EnergyMetricsManager(
        output_dir=output_dir,
        host_cluster=host_cluster,
        docker_manager=docker_manager,
        consolidation_engine=consolidation_engine
    )
    
    # Deploy initial workloads
    logger.info("\n[6/7] Deploying initial workloads...")
    workloads = create_sample_workloads()
    placement_decisions = scheduler.schedule_batch(workloads)
    
    successful_placements = len([d for d in placement_decisions if d is not None])
    logger.info(f"  Successfully placed: {successful_placements}/{len(workloads)} containers")
    
    # Show initial cluster state
    logger.info("\n[7/7] Initial cluster state:")
    initial_summary = host_cluster.get_cluster_summary()
    for key, value in initial_summary.items():
        logger.info(f"  {key}: {value}")
    
    # Run simulation cycles
    logger.info("\n" + "=" * 70)
    logger.info("STARTING SIMULATION CYCLES")
    logger.info("=" * 70)
    
    for cycle in range(1, num_cycles + 1):
        logger.info(f"\n--- Cycle {cycle}/{num_cycles} ---")
        
        # Collect metrics
        metrics = metrics_manager.collect_metrics()
        
        # Log current state
        total_power = sum(m.power_watts for m in metrics)
        active_hosts = len([m for m in metrics if m.state == "active"])
        total_containers = sum(m.active_containers for m in metrics)
        
        logger.info(
            f"  Power: {total_power:.2f}W | "
            f"Active Hosts: {active_hosts} | "
            f"Containers: {total_containers}"
        )
        
        # Run consolidation periodically
        if cycle % consolidation_interval == 0:
            logger.info(f"\n  >>> Running consolidation (cycle {cycle})...")
            result = consolidation_engine.consolidate_threshold_based()
            
            if result.containers_migrated > 0:
                logger.info(
                    f"  Consolidation: {result.containers_migrated} migrations, "
                    f"{result.hosts_consolidated} hosts shutdown, "
                    f"{result.energy_saved_watts:.2f}W saved"
                )
            else:
                logger.info("  No consolidation needed")
        
        # Simulate workload changes (add/remove containers occasionally)
        if cycle == num_cycles // 3:
            logger.info("\n  >>> Adding new workload...")
            new_workload = {
                'name': f'dynamic-{cycle}',
                'image': 'nginx:latest',
                'cpu_request': round(random.uniform(0.5, 1.5), 2),
                'memory_request_gb': round(random.uniform(1.0, 2.0), 2),
                'sla_tier': 'silver'
            }
            scheduler.schedule_container(**new_workload)
        
        if cycle == 2 * num_cycles // 3:
            logger.info("\n  >>> Removing a container...")
            containers = docker_manager.get_running_containers()
            if containers:
                container_to_remove = random.choice(containers)
                docker_manager.remove_container(container_to_remove.container_id)
                
                # Update host tracking
                host = host_cluster.get_host(container_to_remove.host_id)
                if host:
                    host.remove_container(container_to_remove.container_id)
        
        # Shutdown idle hosts
        idle_count = consolidation_engine.shutdown_idle_hosts()
        if idle_count > 0:
            logger.info(f"  Shut down {idle_count} idle host(s)")
        
        # Delay between cycles
        time.sleep(0.5)
    
    # Generate final reports
    logger.info("\n" + "=" * 70)
    logger.info("GENERATING REPORTS AND VISUALIZATIONS")
    logger.info("=" * 70)
    
    logger.info("\nSaving JSON logs...")
    metrics_manager.save_json_log()
    
    logger.info("\nGenerating visualizations...")
    metrics_manager.generate_visualizations()
    
    logger.info("\nGenerating summary report...")
    report_path = metrics_manager.generate_summary_report()
    
    logger.info("\nExporting KPIs...")
    kpis_path = metrics_manager.export_kpis_json()
    
    # Display final statistics
    logger.info("\n" + "=" * 70)
    logger.info("FINAL STATISTICS")
    logger.info("=" * 70)
    
    final_summary = host_cluster.get_cluster_summary()
    logger.info("\nCluster Summary:")
    for key, value in final_summary.items():
        logger.info(f"  {key}: {value}")
    
    consolidation_stats = consolidation_engine.get_statistics()
    logger.info("\nConsolidation Statistics:")
    for key, value in consolidation_stats.items():
        logger.info(f"  {key}: {value}")
    
    scheduler_stats = scheduler.get_placement_statistics()
    logger.info("\nScheduler Statistics:")
    for key, value in scheduler_stats.items():
        if key != 'recent_placements':  # Skip detailed list
            logger.info(f"  {key}: {value}")
    
    kpis = metrics_manager.calculate_kpis()
    logger.info("\nKey Performance Indicators:")
    logger.info(f"  Total Energy: {kpis.get('total_energy_wh', 0):.2f} Wh")
    logger.info(f"  Average Power: {kpis.get('average_power_watts', 0):.2f} W")
    logger.info(f"  Avg CPU Utilization: {kpis.get('average_cpu_utilization', 0)*100:.2f}%")
    logger.info(f"  Avg Power per Container: {kpis.get('average_power_per_container', 0):.2f} W")
    
    # Show output files
    logger.info("\n" + "=" * 70)
    logger.info("OUTPUT FILES")
    logger.info("=" * 70)
    logger.info(f"  CSV Log: {metrics_manager.csv_log_path}")
    logger.info(f"  JSON Log: {metrics_manager.json_log_path}")
    logger.info(f"  Summary Report: {report_path}")
    logger.info(f"  KPIs JSON: {kpis_path}")
    logger.info(f"  Visualizations: {metrics_manager.visuals_dir}")
    
    logger.info("\n" + "=" * 70)
    logger.info("SIMULATION COMPLETE")
    logger.info("=" * 70)
    
    print("\n✅ Simulation completed successfully!")
    print(f"📊 Check output files in: {output_dir}")
    print(f"📈 Visualizations available in: {metrics_manager.visuals_dir}")
    print(f"📄 Summary report: {report_path}")


def main():
    """Main entry point."""
    try:
        # Configuration
        NUM_HOSTS = 5
        NUM_CYCLES = 10
        CONSOLIDATION_INTERVAL = 3
        USE_REAL_DOCKER = False  # Set to True to use real Docker
        
        # Run simulation
        run_simulation(
            num_hosts=NUM_HOSTS,
            num_cycles=NUM_CYCLES,
            consolidation_interval=CONSOLIDATION_INTERVAL,
            use_real_docker=USE_REAL_DOCKER
        )
        
    except KeyboardInterrupt:
        logger.info("\n\nSimulation interrupted by user")
        print("\n⚠️  Simulation interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n\nSimulation failed with error: {e}", exc_info=True)
        print(f"\n❌ Simulation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

