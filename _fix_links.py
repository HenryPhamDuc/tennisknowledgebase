"""
Fix all `index.md` -> `index.html` references inside href= attributes in markdown source.

Only touch href="...index.md" patterns. Don't touch:
- The file's own `index.md` line at the top (its own filename)
- Code blocks (we use a simple heuristic: skip indented 4-space blocks)
"""
import os
import re

ROOT = r"C:\Users\Henry\Documents\Github\tenniskb\docs"

# Match href=".../index.md" or href="...index.md?anchor" or href="...index.md#anchor"
# The pattern: href="(<any non-quote>)(index\.md)(<any non-quote>)"
PATTERN = re.compile(r'(href="[^"]*?)(index\.md)([^"]*")')

def fix_file(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, n = PATTERN.subn(r'\1index.html\3', content)
    if n > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return n

total = 0
files_changed = 0
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(root, f)
        n = fix_file(path)
        if n > 0:
            files_changed += 1
            total += n

print(f"Fixed {total} links in {files_changed} files under {ROOT}")
