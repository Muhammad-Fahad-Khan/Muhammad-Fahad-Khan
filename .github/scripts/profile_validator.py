import re
import requests
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_urls(text):
    urls = set()
    patterns = [
        r'https?://[^\s)\]"\']+',
        r'\[[^\]]+\]\((https?://[^\)]+)\)',
        r'href=["\'](https?://[^"\']+)["\']',
        r'src=["\'](https?://[^"\']+)["\']',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            url = match.group(1) if match.lastindex else match.group(0)
            urls.add(url.rstrip(").,>"))
    return sorted(urls)

def url_ok(url):
    try:
        r = requests.head(url, timeout=8, allow_redirects=True, headers=HEADERS)
        if r.status_code >= 400:
            r = requests.get(url, timeout=10, allow_redirects=True, headers=HEADERS)
        return r.status_code < 400, r.status_code
    except Exception:
        try:
            r = requests.get(url, timeout=10, allow_redirects=True, headers=HEADERS)
            return r.status_code < 400, r.status_code
        except Exception:
            return False, 0

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

urls = extract_urls(readme)
report = {"total": len(urls), "broken": []}

for url in urls:
    ok, status = url_ok(url)
    if not ok:
        report["broken"].append({"url": url, "status": status})

with open(".github/validation_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"Validated {len(urls)} links")
print(f"Broken: {len(report['broken'])}")
if report["broken"]:
    for item in report["broken"]:
        print(f"Broken -> {item['url']} ({item['status']})")
