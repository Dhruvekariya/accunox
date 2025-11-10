# Problem Statement 2: System Monitoring Scripts

This directory contains two monitoring scripts implemented in Python for system and application health monitoring.

## Scripts Overview

### 1. Application Health Checker (`app_health_checker.py`)
Monitors application uptime by checking HTTP status codes to determine if applications are functioning correctly.

### 2. System Health Monitor (`system_health_monitor.py`)
Monitors system resources (CPU, memory, disk, processes) and generates alerts when thresholds are exceeded.

---

## Script 1: Application Health Checker

### Features
- Check single or multiple application URLs
- HTTP status code analysis (200-599)
- Determines application status: UP, DOWN, or UNKNOWN
- Support for continuous monitoring
- Read URLs from file
- Configurable timeout
- Color-coded console output
- Summary reporting

### Usage

#### Basic Usage
```bash
# Check single application
python3 app_health_checker.py https://example.com

# Check multiple applications
python3 app_health_checker.py https://google.com https://github.com https://localhost:8080
```

#### From File
```bash
# Create urls.txt with one URL per line
cat > urls.txt <<EOF
https://google.com
https://github.com
https://example.com
EOF

# Check all URLs from file
python3 app_health_checker.py --file urls.txt
```

#### Continuous Monitoring
```bash
# Monitor every 60 seconds (default)
python3 app_health_checker.py --continuous https://example.com

# Monitor every 30 seconds
python3 app_health_checker.py --continuous --interval 30 https://example.com
```

#### Custom Timeout
```bash
# Set 10-second timeout for slow servers
python3 app_health_checker.py --timeout 10 https://slow-server.com
```

### Command Line Options
```
usage: app_health_checker.py [-h] [--file FILE] [--continuous]
                              [--interval INTERVAL] [--timeout TIMEOUT]
                              [urls ...]

positional arguments:
  urls                  URLs to check

optional arguments:
  --file, -f FILE       File containing URLs (one per line)
  --continuous, -c      Continuously monitor (requires single URL)
  --interval, -i        Check interval in seconds (default: 60)
  --timeout, -t         Request timeout in seconds (default: 5)
```

### Status Codes Interpretation
- **200-299:** UP - Application functioning correctly
- **300-399:** UP - Application up (redirect)
- **400-499:** DOWN - Client error
- **500-599:** DOWN - Server error
- **TIMEOUT:** DOWN - Request timeout
- **ERROR:** DOWN - Connection or other error

### Example Output
```
======================================================================
APPLICATION HEALTH CHECK REPORT
======================================================================

[✓] https://github.com
    Status: UP
    HTTP Code: 200
    Message: Application is functioning correctly
    Checked at: 2025-11-07 20:43:22

[✗] https://nonexistent.example.com
    Status: DOWN
    HTTP Code: N/A
    Message: Unable to connect or receive response
    Checked at: 2025-11-07 20:43:22

======================================================================
SUMMARY: 1 UP | 1 DOWN | Total: 2
======================================================================
```

---

## Script 2: System Health Monitor

### Features
- Monitor CPU usage
- Monitor memory usage
- Monitor disk space
- Display top CPU-consuming processes
- Configurable thresholds
- Alert system for exceeded thresholds
- Continuous monitoring mode
- Log to file option
- Color-coded console output
- Cross-platform (Linux & macOS)

### Usage

#### Basic Usage
```bash
# One-time system health check
python3 system_health_monitor.py
```

#### Continuous Monitoring
```bash
# Monitor every 60 seconds (default)
python3 system_health_monitor.py --continuous

# Monitor every 30 seconds
python3 system_health_monitor.py --continuous --interval 30
```

#### Custom Thresholds
```bash
# Set custom thresholds: CPU=90%, Memory=85%, Disk=80%
python3 system_health_monitor.py --thresholds cpu=90,memory=85,disk=80
```

#### Log to File
```bash
# One-time check with logging
python3 system_health_monitor.py --log /var/log/system_health.log

# Continuous monitoring with logging
python3 system_health_monitor.py --continuous --interval 60 --log health.log
```

### Command Line Options
```
usage: system_health_monitor.py [-h] [--continuous] [--interval INTERVAL]
                                 [--log LOG] [--thresholds THRESHOLDS]

optional arguments:
  --continuous, -c          Continuously monitor system health
  --interval, -i INTERVAL   Check interval in seconds (default: 60)
  --log, -l LOG            Log file path for alerts and reports
  --thresholds, -t         Custom thresholds (e.g., cpu=90,memory=85,disk=80)
```

### Default Thresholds
- **CPU:** 80%
- **Memory:** 80%
- **Disk:** 80%

### Example Output
```
======================================================================
SYSTEM HEALTH MONITORING REPORT
Timestamp: 2025-11-07 20:43:51
======================================================================

SYSTEM METRICS:
  CPU Usage:    10.9%
  Memory Usage: 99.7%
  Disk Usage:   25.0%

TOP CPU-CONSUMING PROCESSES:
  PID      CPU%   MEM%   USER       COMMAND
  ------------------------------------------------------------
  602      12.5   0.1    root       /usr/libexec/opendirectoryd
  635      9.6    0.9    _windowserver /System/Library/PrivateFrameworks/SkyLight.framewo
  99822    8.2    3.7    dhruvvekariya claude
  25744    6.6    11.9   dhruvvekariya /Applications/OrbStack.app/Contents/Frameworks/Orb

⚠ ALERTS:
  ✗ Memory usage is HIGH: 99.7% (threshold: 80%)
======================================================================
```

---

## Installation & Requirements

### Prerequisites
- Python 3.6+
- curl (for app_health_checker.py)
- Standard Unix tools (ps, top, df, etc.)

### No External Dependencies
Both scripts use only Python standard library and system commands - no pip install required!

### Setup
```bash
# Make scripts executable
chmod +x app_health_checker.py system_health_monitor.py

# Test application health checker
./app_health_checker.py https://google.com

# Test system health monitor
./system_health_monitor.py
```

---

## Use Cases

### Application Health Checker
1. **Website Monitoring:** Check if your websites are accessible
2. **API Health Checks:** Monitor API endpoints
3. **Load Balancer Checks:** Verify backend servers are responding
4. **Deployment Verification:** Ensure applications are running after deployment
5. **Continuous Monitoring:** Set up cron jobs or systemd timers

### System Health Monitor
1. **Server Monitoring:** Track resource usage on production servers
2. **Alert System:** Get notified when resources are running low
3. **Performance Troubleshooting:** Identify resource-hungry processes
4. **Capacity Planning:** Historical data for resource trends
5. **Automated Checks:** Run via cron for periodic monitoring

---

## Automation Examples

### Cron Job - Application Health Check
```bash
# Check every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/app_health_checker.py https://myapp.com >> /var/log/app_health.log 2>&1
```

### Cron Job - System Health Monitor
```bash
# Check every hour
0 * * * * /usr/bin/python3 /path/to/system_health_monitor.py --log /var/log/system_health.log
```

### Systemd Service - Continuous Monitoring
```ini
[Unit]
Description=System Health Monitor
After=network.target

[Service]
Type=simple
User=monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/system_health_monitor.py --continuous --interval 60 --log /var/log/system_health.log
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Testing

### Test Application Health Checker
```bash
# Test with known-good URLs
python3 app_health_checker.py https://google.com https://github.com

# Test with local Wisecow app (if running)
python3 app_health_checker.py http://localhost:8080

# Test with non-existent URL (should show DOWN)
python3 app_health_checker.py https://this-does-not-exist-12345.com
```

### Test System Health Monitor
```bash
# Basic test
python3 system_health_monitor.py

# Test with lower thresholds to trigger alerts
python3 system_health_monitor.py --thresholds cpu=5,memory=5,disk=5

# Test logging
python3 system_health_monitor.py --log test.log && cat test.log
```

---

## Troubleshooting

### Application Health Checker

**Issue:** "curl: command not found"
- **Solution:** Install curl: `apt install curl` (Linux) or `brew install curl` (macOS)

**Issue:** SSL certificate errors
- **Solution:** The script uses `--insecure` flag to bypass certificate validation

### System Health Monitor

**Issue:** Permission denied reading system files
- **Solution:** Run with appropriate permissions or use sudo

**Issue:** High memory usage reported incorrectly
- **Solution:** This is normal for macOS/Linux which uses memory efficiently

---

## Architecture & Design

### Application Health Checker
- Uses `curl` subprocess for HTTP requests
- Timeout handling to prevent hanging
- Status code categorization logic
- Modular design for easy extension

### System Health Monitor
- Cross-platform support (Linux & macOS)
- Uses native system commands (top, ps, df, vm_stat)
- Graceful fallbacks for missing data
- Configurable alerting system

---

## License

These scripts are created for the Accuknox DevOps Trainee Assessment.

## Author

DevOps Assessment - Problem Statement 2 Implementation
