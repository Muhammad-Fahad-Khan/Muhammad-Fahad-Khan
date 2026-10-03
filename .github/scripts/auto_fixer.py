import json
import re
from datetime import datetime

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_whitespace(content):
    return re.sub(r" {2,}", " ", content)

def add_maintenance_comment(content):
    stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    marker = f"<!-- Last Maintenance: {stamp} -->"
    if "<!-- Last Maintenance:" in content:
        content = re.sub(r"<!-- Last Maintenance: .*? -->", marker, content)
    else:
        content = marker + "\n" + content
    return content

def fix_common_issues(content):
    content = fix_whitespace(content)
    content = add_maintenance_comment(content)

    # Make sure the main sections still exist
    required = [
        "## 👋 About Me",
        "## 🛠️ Tech Stack",
        "## 📊 GitHub Stats",
        "## 🏆 Featured Projects",
        "## 🚀 Live Projects",
    ]
    for section in required:
        if section not in content:
            content += f"\n\n{section}\n"
    return content

try:
    with open(".github/validation_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
except FileNotFoundError:
    report = {"broken": []}

content = read("README.md")
fixed = fix_common_issues(content)
write("README.md", fixed)

print("Auto-fix complete.")
if report.get("broken"):
    print(f"Detected {len(report['broken'])} broken links. Review recommended.")
