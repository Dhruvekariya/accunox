#!/usr/bin/env python3
"""
Application Health Checker Script

This script checks the uptime and health of applications by making HTTP requests
and analyzing the status codes to determine if the application is 'up' or 'down'.

Usage:
    python3 app_health_checker.py <url1> <url2> ...
    python3 app_health_checker.py --file urls.txt
    python3 app_health_checker.py --continuous --interval 60 <url>

Author: DevOps Assessment
"""

import sys
import time
import argparse
from datetime import datetime
from urllib.parse import urlparse
import subprocess

def check_application_health(url, timeout=5):
    """
    Check if an application is up by making an HTTP request.

    Args:
        url (str): The URL to check
        timeout (int): Request timeout in seconds

    Returns:
        dict: Health check result with status, status_code, and message
    """
    try:
        # Use curl for the HTTP request (cross-platform compatible)
        cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
               '--max-time', str(timeout), '--insecure', url]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+2)
        status_code = result.stdout.strip()

        if not status_code or not status_code.isdigit():
            return {
                'url': url,
                'status': 'DOWN',
                'status_code': 'N/A',
                'message': 'Unable to connect or receive response',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        status_code = int(status_code)

        # Determine if application is UP or DOWN based on status code
        if 200 <= status_code < 300:
            status = 'UP'
            message = 'Application is functioning correctly'
        elif 300 <= status_code < 400:
            status = 'UP'
            message = 'Application is up (redirect)'
        elif 400 <= status_code < 500:
            status = 'DOWN'
            message = f'Client error (HTTP {status_code})'
        elif 500 <= status_code < 600:
            status = 'DOWN'
            message = f'Server error (HTTP {status_code})'
        else:
            status = 'UNKNOWN'
            message = f'Unexpected status code: {status_code}'

        return {
            'url': url,
            'status': status,
            'status_code': status_code,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except subprocess.TimeoutExpired:
        return {
            'url': url,
            'status': 'DOWN',
            'status_code': 'TIMEOUT',
            'message': f'Request timeout after {timeout} seconds',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {
            'url': url,
            'status': 'DOWN',
            'status_code': 'ERROR',
            'message': f'Error: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def format_result(result):
    """Format health check result for display."""
    status_symbol = '✓' if result['status'] == 'UP' else '✗'
    status_color = '\033[92m' if result['status'] == 'UP' else '\033[91m'
    reset_color = '\033[0m'

    return f"""
{status_color}[{status_symbol}] {result['url']}{reset_color}
    Status: {result['status']}
    HTTP Code: {result['status_code']}
    Message: {result['message']}
    Checked at: {result['timestamp']}
"""

def check_multiple_urls(urls, timeout=5):
    """Check health of multiple URLs."""
    results = []
    print("=" * 70)
    print("APPLICATION HEALTH CHECK REPORT")
    print("=" * 70)

    for url in urls:
        result = check_application_health(url, timeout)
        results.append(result)
        print(format_result(result))

    # Summary
    up_count = sum(1 for r in results if r['status'] == 'UP')
    down_count = sum(1 for r in results if r['status'] == 'DOWN')

    print("=" * 70)
    print(f"SUMMARY: {up_count} UP | {down_count} DOWN | Total: {len(results)}")
    print("=" * 70)

    return results

def continuous_monitor(url, interval=60, timeout=5):
    """Continuously monitor a URL at specified intervals."""
    print(f"Starting continuous monitoring of {url}")
    print(f"Check interval: {interval} seconds")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            result = check_application_health(url, timeout)
            print(format_result(result))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")

def read_urls_from_file(filename):
    """Read URLs from a file (one per line)."""
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Application Health Checker - Check if applications are up or down',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com https://google.com
  %(prog)s --file urls.txt
  %(prog)s --continuous --interval 30 https://example.com
  %(prog)s --timeout 10 https://slow-server.com
        """
    )

    parser.add_argument('urls', nargs='*', help='URLs to check')
    parser.add_argument('--file', '-f', help='File containing URLs (one per line)')
    parser.add_argument('--continuous', '-c', action='store_true',
                        help='Continuously monitor (requires single URL)')
    parser.add_argument('--interval', '-i', type=int, default=60,
                        help='Check interval in seconds for continuous mode (default: 60)')
    parser.add_argument('--timeout', '-t', type=int, default=5,
                        help='Request timeout in seconds (default: 5)')

    args = parser.parse_args()

    # Determine URLs to check
    if args.file:
        urls = read_urls_from_file(args.file)
    elif args.urls:
        urls = args.urls
    else:
        parser.print_help()
        sys.exit(1)

    if not urls:
        print("Error: No URLs provided")
        sys.exit(1)

    # Continuous monitoring mode
    if args.continuous:
        if len(urls) > 1:
            print("Error: Continuous mode requires exactly one URL")
            sys.exit(1)
        continuous_monitor(urls[0], args.interval, args.timeout)
    else:
        # One-time check
        check_multiple_urls(urls, args.timeout)

if __name__ == '__main__':
    main()
