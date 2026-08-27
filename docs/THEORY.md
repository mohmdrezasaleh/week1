# Server Sentinel Theory

## 1. Idempotency

### What is Idempotency?

Idempotency means that running the same operation multiple times produces the same intended system state without causing unintended side effects.

In DevOps and automation, scripts should ideally be safe to execute repeatedly.

### Example in Server Sentinel

The Server Sentinel project is designed to automate server maintenance tasks.

For example:

- Checking system health repeatedly should not modify the system.
- Checking the Nginx service status repeatedly should not cause unnecessary changes.
- Nginx should only be restarted when it is detected as inactive.
- Backup cleanup should only remove archives older than the configured retention period.

A non-idempotent operation can create unexpected results when executed multiple times.

---

## 2. Bash vs Python

### Bash

Bash is useful for Linux system automation and command execution.

Advantages:

- Native access to Linux commands.
- Useful for file operations and service management.
- Lightweight and simple for shell automation.
- Works well with commands such as `tar`, `find`, `df`, and `systemctl`.

In Server Sentinel, Bash is used for:

- System health checks.
- Nginx service management.
- Backup creation.
- Backup retention cleanup.
- Module orchestration.

### Python

Python is useful when more structured data processing and analysis are required.

Advantages:

- Easier parsing and data processing.
- Better data structures.
- Easier error handling.
- Suitable for generating structured output and reports.

In Server Sentinel, Python is used for:

- Nginx access log analysis.
- HTTP status code aggregation.
- Client IP analysis.
- Security anomaly detection.
- Report generation.

### Why Use Both?

The project uses a hybrid approach.

Bash is used for direct interaction with the Linux operating system, while Python is used for data processing and reporting.

This approach allows each language to be used for the tasks where it is most suitable.

---

## 3. Nginx Architecture

Nginx is a web server and reverse proxy designed to handle multiple concurrent connections efficiently.

### Basic Request Flow

```text
Client
   |
   v
Nginx
   |
   +--> Static Content
   |
   +--> Reverse Proxy / Application