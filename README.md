# Operation Sentinel

A modular Linux server monitoring and management tool built with **Bash** and **Python**.

---

## Overview
Automates basic server monitoring and log analyzer.

The main script performs:

- System health checks
- Nginx status checks & auto-healing
- backup creation and cleanup
- Nginx access log analysis
- Report modules and web publishing

## Project Structure

```text
.
├── main.sh
├── modules/
│   ├── health.sh
│   ├── backup.sh
│   ├── log_analyzer.py
│   └── reporter.py
├── docs/
│   └── THEORY.md
└── README.md
```

## Requirements

- Linux
- Bash
- Python

## Installation

Clone the repository:

```bash
git clone http://195.24.237.134/devops/week1.git
cd week1
```

Make the Bash scripts executable:

```bash
chmod +x main.sh
chmod +x modules/*.sh
```

## Usage

Run the complete Server Sentinel workflow:

```bash
./main.sh
```

Execution flow:

```text
main.sh
   ↓
health.sh
   ↓
backup.sh
   ↓
log_analyzer.py
   ↓
reporter.py
```

---

## Modules


**Backup**

```modules/backup.sh```

Creates compressed backups of:

```text
/etc/nginx/
/var/www/html/
```

Backup format:

```text
backup_YYYY-MM-DD_HHMM.tar.gz
```

Backups older than 3 days are automatically **removed**.

---

**Log Analyzer**

```modules/log_analyzer.py```

Analyzes:
```text
/var/log/nginx/access.log
```

The analyzer provides:

- Total request count
- Top 5 client IP addresses
- HTTP status code summary
- 401/403 security threat detection

Results are saved for use by the reporting module.

---

## Documentation

Additional technical documentation is available in:

```docs/THEORY.md```

It covers:

- Idempotency
- **Bash** vs **Python** trade-offs
- **Nginx** architecture

---