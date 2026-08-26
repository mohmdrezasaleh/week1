import os
import json
from collections import Counter

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

LOG_FILE = "/var/log/nginx/access.log"
OUTPUT_FILE = "data/log_analysis.json"

SECURITY_THRESHOLD = 50

def read_log():
    """"Reading Nginx access log and return lines."""
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError(f"Log file not found: {LOG_FILE}")

    with open(LOG_FILE, "r") as file:
        return file.readlines()

def parse_line(line):
    """"Extracting clinet IPs and HTTP status code from one log line"""
    parts = line.split()

    if len(parts) < 9 :
        return None

    ip = parts[0]
    status = int(parts[8])

    return {
        "ip": ip,
        "status": status
    }

def analyze_logs(lines):
    """"Analyze IP addressess and HTTP status codes"""
    ip_counter = Counter()

    status_codes = {
        "2xx": 0,
        "3xx": 0,
        "4xx": 0,
        "5xx": 0
    }

    status_401 = 0
    status_403 = 0

    parsed_lines = 0
    invalid_lines = 0

    for line in lines:
        result = parse_line(line)

        if result is None:
            invalid_lines += 1
            continue

        parsed_lines += 1

        ip = result["ip"]
        status = result["status"]

        ip_counter[ip] += 1

        if 200 <= status < 300:
            status_codes["2xx"] += 1

        elif 300 <= status < 400:
            status_codes["3xx"] += 1

        elif 400 <= status < 500:
            status_codes["4xx"] += 1

        elif 500 <= status < 600:
            status_codes["5xx"] += 1

        if status == 401:
            status_401 += 1

        elif status == 403:
            status_403 += 1

    top_ips = [
        {
            "ip": ip,
            "requests": count
        }
        for ip, count in ip_counter.most_common(5)
    ]

    return {
        "total_requests": parsed_lines,
        "invalid_lines": invalid_lines,
        "top_ips": top_ips,
        "status_codes": status_codes,
        "security_counts": {
            "401": status_401,
            "403": status_403}
       }       

def detect_status(analysis):
    """Detecting security codes based on 401/403 counts"""
    alerts = []
    
    count_401 = analysis["security_counts"]["401"]
    count_403 = analysis["security_counts"]["403"]

    if count_401 > SECURITY_THRESHOLD:
        alerts.append(
            f"{YELLOW}High number of 401 Unauthorized responses detected:{RESET} {count_401}"
        )

    if count_403 > SECURITY_THRESHOLD:
        alerts.append(
            f"{YELLOW}High number of 403 Forbidden responses detected:{RESET} {count_403}"
        )

    return alerts

def main():
    """main Program function"""
    try:
        lines = read_log()

        analysis = analyze_logs(lines)

        alerts = detect_status(analysis)

        analysis["security_alerts"] = alerts

        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(analysis, file, indent=4)

        print(f"{GREEN}Nginx log analysis completed.{RESET}")
        print(f"Total requests: {analysis['total_requests']}")
        print(f"Invalid lines: {analysis['invalid_lines']}")

        print("\nTop 5 IPs:")
        for item in analysis["top_ips"]:
            print(f"  {item['ip']} -> {item['requests']} requests")

        print("\nHTTP Status Codes:")
        for status, count in analysis["status_codes"].items():
            print(f"  {status}: {count}")

        print("\nSecurity:")
        if alerts:
            for alert in alerts:
                print(f"  [WARNING] {alert}")
        else:
            print("  {GREEN}[OK] No security threats detected.{RESET}")

        print(f"\nOutput saved to: {OUTPUT_FILE}")

    except FileNotFoundError as error:
        print(f"[ERROR] {RED}{error}{RESET}")
        raise SystemExit(1)

    except PermissionError:
        print(f"[ERROR] {RED}Permission denied:{RESET} {LOG_FILE}")
        print("Try running the script with sudo.")
        raise SystemExit(1)            

if __name__ == "__main__":
    main()
