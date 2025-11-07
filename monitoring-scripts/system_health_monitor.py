#!/usr/bin/env python3
"""
System Health Monitoring Script

This script monitors the health of a Linux/macOS system by checking:
- CPU usage
- Memory usage
- Disk space
- Running processes

If any metric exceeds predefined thresholds, an alert is sent to the console or a log file.

Usage:
    python3 system_health_monitor.py
    python3 system_health_monitor.py --log /var/log/system_health.log
    python3 system_health_monitor.py --continuous --interval 30
    python3 system_health_monitor.py --thresholds cpu=90,memory=85,disk=80

Author: DevOps Assessment
"""

import sys
import time
import argparse
import subprocess
import platform
from datetime import datetime

# Default thresholds (percentage)
DEFAULT_THRESHOLDS = {
    'cpu': 80,
    'memory': 80,
    'disk': 80
}

def get_cpu_usage():
    """Get current CPU usage percentage."""
    try:
        if platform.system() == 'Darwin':  # macOS
            # Using top command for macOS
            cmd = "top -l 1 | grep 'CPU usage' | awk '{print $3}' | sed 's/%//'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return float(result.stdout.strip())
        else:  # Linux
            # Using top command for Linux
            cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | sed 's/%us,//'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return float(result.stdout.strip())
    except:
        # Fallback: parse /proc/stat on Linux
        try:
            with open('/proc/loadavg', 'r') as f:
                load = float(f.read().split()[0])
                return min(load * 25, 100)  # Rough estimate
        except:
            return 0.0

def get_memory_usage():
    """Get current memory usage percentage."""
    try:
        if platform.system() == 'Darwin':  # macOS
            # Get total memory
            cmd_total = "sysctl -n hw.memsize"
            total = int(subprocess.run(cmd_total, shell=True, capture_output=True, text=True).stdout.strip())

            # Get free memory
            cmd_free = "vm_stat | grep 'Pages free' | awk '{print $3}' | sed 's/\\.//'"
            free_pages = int(subprocess.run(cmd_free, shell=True, capture_output=True, text=True).stdout.strip())

            page_size = 4096  # macOS page size
            free_memory = free_pages * page_size
            used_memory = total - free_memory
            usage = (used_memory / total) * 100
            return round(usage, 2)
        else:  # Linux
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                mem_total = int([l for l in lines if 'MemTotal' in l][0].split()[1])
                mem_available = int([l for l in lines if 'MemAvailable' in l][0].split()[1])
                usage = ((mem_total - mem_available) / mem_total) * 100
                return round(usage, 2)
    except:
        return 0.0

def get_disk_usage():
    """Get disk usage percentage for root partition."""
    try:
        cmd = "df -h / | tail -1 | awk '{print $5}' | sed 's/%//'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0.0

def get_top_processes(count=5):
    """Get top CPU-consuming processes."""
    try:
        if platform.system() == 'Darwin':  # macOS
            cmd = f"ps aux | sort -rk 3 | head -{count+1} | tail -{count}"
        else:  # Linux
            cmd = f"ps aux --sort=-%cpu | head -{count+1} | tail -{count}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')

        processes = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    'user': parts[0],
                    'pid': parts[1],
                    'cpu': parts[2],
                    'mem': parts[3],
                    'command': ' '.join(parts[10:])[:50]
                })
        return processes
    except:
        return []

def check_system_health(thresholds):
    """Check system health against thresholds."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get metrics
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    top_processes = get_top_processes(5)

    # Check thresholds
    alerts = []

    if cpu_usage > thresholds['cpu']:
        alerts.append(f"CPU usage is HIGH: {cpu_usage:.1f}% (threshold: {thresholds['cpu']}%)")

    if memory_usage > thresholds['memory']:
        alerts.append(f"Memory usage is HIGH: {memory_usage:.1f}% (threshold: {thresholds['memory']}%)")

    if disk_usage > thresholds['disk']:
        alerts.append(f"Disk usage is HIGH: {disk_usage:.1f}% (threshold: {thresholds['disk']}%)")

    return {
        'timestamp': timestamp,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'top_processes': top_processes,
        'alerts': alerts
    }

def format_report(health_data):
    """Format health check data into a readable report."""
    report = []

    # Header
    report.append("=" * 70)
    report.append("SYSTEM HEALTH MONITORING REPORT")
    report.append(f"Timestamp: {health_data['timestamp']}")
    report.append("=" * 70)
    report.append("")

    # Metrics
    report.append("SYSTEM METRICS:")
    report.append(f"  CPU Usage:    {health_data['cpu_usage']:.1f}%")
    report.append(f"  Memory Usage: {health_data['memory_usage']:.1f}%")
    report.append(f"  Disk Usage:   {health_data['disk_usage']:.1f}%")
    report.append("")

    # Top Processes
    if health_data['top_processes']:
        report.append("TOP CPU-CONSUMING PROCESSES:")
        report.append(f"  {'PID':<8} {'CPU%':<6} {'MEM%':<6} {'USER':<10} {'COMMAND'}")
        report.append("  " + "-" * 60)
        for proc in health_data['top_processes']:
            report.append(f"  {proc['pid']:<8} {proc['cpu']:<6} {proc['mem']:<6} {proc['user']:<10} {proc['command']}")
        report.append("")

    # Alerts
    if health_data['alerts']:
        report.append("\033[91m" + "⚠ ALERTS:" + "\033[0m")
        for alert in health_data['alerts']:
            report.append(f"  \033[91m✗ {alert}\033[0m")
    else:
        report.append("\033[92m" + "✓ No alerts - All metrics within thresholds" + "\033[0m")

    report.append("=" * 70)
    report.append("")

    return '\n'.join(report)

def log_to_file(report, log_file):
    """Append report to log file."""
    try:
        with open(log_file, 'a') as f:
            # Remove color codes for log file
            clean_report = report.replace('\033[91m', '').replace('\033[92m', '').replace('\033[0m', '')
            f.write(clean_report + '\n')
        print(f"Report logged to: {log_file}")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def continuous_monitor(interval, thresholds, log_file=None):
    """Continuously monitor system health at specified intervals."""
    print(f"Starting continuous system health monitoring")
    print(f"Check interval: {interval} seconds")
    print(f"Thresholds: CPU={thresholds['cpu']}%, Memory={thresholds['memory']}%, Disk={thresholds['disk']}%")
    if log_file:
        print(f"Logging to: {log_file}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            health_data = check_system_health(thresholds)
            report = format_report(health_data)
            print(report)

            if log_file:
                log_to_file(report, log_file)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")

def parse_thresholds(threshold_str):
    """Parse threshold string like 'cpu=90,memory=85,disk=80'."""
    thresholds = DEFAULT_THRESHOLDS.copy()

    if threshold_str:
        for pair in threshold_str.split(','):
            key, value = pair.split('=')
            thresholds[key.strip()] = int(value.strip())

    return thresholds

def main():
    parser = argparse.ArgumentParser(
        description='System Health Monitor - Monitor CPU, Memory, Disk, and Processes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --log /var/log/system_health.log
  %(prog)s --continuous --interval 30
  %(prog)s --thresholds cpu=90,memory=85,disk=80
  %(prog)s --continuous --interval 60 --log health.log

Default thresholds: CPU=80%%, Memory=80%%, Disk=80%%
        """
    )

    parser.add_argument('--continuous', '-c', action='store_true',
                        help='Continuously monitor system health')
    parser.add_argument('--interval', '-i', type=int, default=60,
                        help='Check interval in seconds for continuous mode (default: 60)')
    parser.add_argument('--log', '-l', help='Log file path for alerts and reports')
    parser.add_argument('--thresholds', '-t',
                        help='Custom thresholds (e.g., cpu=90,memory=85,disk=80)')

    args = parser.parse_args()

    # Parse thresholds
    thresholds = parse_thresholds(args.thresholds)

    if args.continuous:
        # Continuous monitoring mode
        continuous_monitor(args.interval, thresholds, args.log)
    else:
        # One-time check
        health_data = check_system_health(thresholds)
        report = format_report(health_data)
        print(report)

        if args.log:
            log_to_file(report, args.log)

if __name__ == '__main__':
    main()
