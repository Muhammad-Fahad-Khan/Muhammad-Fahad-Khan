import random
import re
from datetime import datetime

quotes = [
    "Efficient, reliable software -- from the code to the Clusters.",
    "Build systems, not just code.",
    "Automate the boring stuff.",
    "Scale with confidence.",
    "Code that lasts.",
]

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

content = read("README.md")

# Add last update marker
stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
marker = f"<!-- Last Automatic Update: {stamp} -->"
if "<!-- Last Automatic Update:" in content:
    content = re.sub(r"<!-- Last Automatic Update: .*? -->", marker, content)
else:
    content = marker + "\n" + content

# Rotate quote
quote = random.choice(quotes)
if '<i>' in content:
    content = re.sub(r'<i>.*?</i>', f'<i>"{quote}"</i>', content, count=1)
else:
    content += f'\n\n<i>"{quote}"</i>\n'

# Ensure HTTPS links
content = content.replace("http://", "https://")

write("README.md", content)
print("Daily update complete.")
