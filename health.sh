#!/usr/bin/env bash
set -euo pipefail

# simple setting :D
limit=80
output="output/health.json"
[[ "${1:-}" == "--output" ]] && output="$2"

# CPU usage
idle=$(top -bn1 | awk '/Cpu\(s\)/ {print $8}')
cpu=$(awk -v idle="$idle" 'BEGIN {printf "%.1f", 100-idle}')

# RAM usage
ram=$(free | awk '/Mem:/ {printf "%.1f", $3/$2*100}')

# Disk usage
disk=$(df -P / | awk 'NR==2 {gsub("%", "", $5); print $5}')

# Warning check
status() {
  awk -v value="$1" -v limit="$limit" 'BEGIN {print (value > limit ? "[WARNING]" : "[OK]")}'
}

# Nginx check
action=none # remove this
if systemctl is-active --quiet nginx; then
  before=active
else
  before=inactive
  systemctl restart nginx
  action=restarted
fi
after=active

mkdir -p "$(dirname "$output")"
printf '{"cpu":{"value":%s,"status":"%s"},"ram":{"value":%s,"status":"%s"},"disk":{"value":%s,"status":"%s"},"nginx":{"before":"%s","action":"%s","after":"%s"}}\n' \
  "$cpu" "$(status "$cpu")" "$ram" "$(status "$ram")" "$disk" "$(status "$disk")" \
  "$before" "$action" "$after" | tee "$output"
