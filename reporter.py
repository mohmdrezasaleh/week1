#!/usr/bin/env python3
import html
import json
from pathlib import Path
from string import Template


def read(name):
    return json.loads(Path(f"output/{name}.json").read_text())


health = read("health")
logs = read("log_analysis")
backup = read("backup")

metrics = "\n".join(
    f"| {name.upper()} | {health[name]['value']}% | {health[name]['status']} |"
    for name in ("cpu", "ram", "disk")
)
codes = "\n".join(f"| {code} | {count} |" for code, count in logs["status_groups"].items())
ips = "\n".join(f"| {item['ip']} | {item['count']} |" for item in logs["top_ips"])
threats = "\n".join(logs["threats"]) or "None"
nginx = health["nginx"]

template_path = Path(__file__).with_name("report_template.md")
report = Template(template_path.read_text()).substitute(
    metrics=metrics,
    nginx=f"{nginx['before']} → {nginx['action']} → {nginx['after']}",
    codes=codes,
    ips=ips,
    threats=threats,
    backup=backup["archive"],
)

Path("report.md").write_text(report)
Path("/var/www/html/index.html").write_text(f"<pre>{html.escape(report)}</pre>")
print("Report created")
