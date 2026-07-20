"""
Audit built site for 404s. For every HTML file:
- Extract all href links
- Resolve them to filesystem paths
- Check the file exists
Report any broken links.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = r"C:\Users\Henry\Documents\Github\tenniskb\site"

# Skip external URLs, anchors-only, mailto, tel
def is_external_or_anchor(url: str) -> bool:
    if not url:
        return True
    if url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return True
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https", "ftp"):
        return True
    return False

# Find all href targets in an HTML file
HREF_PATTERN = re.compile(r'href="([^"]+)"')
# Also check <a href="...">, <link href="...">, <img src="...">, <script src="...">
ATTR_PATTERN = re.compile(r'(?:href|src)="([^"]+)"')

def check_file_links(html_path: str) -> list:
    """Return list of (link, reason) for broken links in html_path."""
    broken = []
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    base_dir = os.path.dirname(html_path)

    for match in ATTR_PATTERN.finditer(content):
        url = match.group(1)
        if is_external_or_anchor(url):
            continue
        # Strip the #anchor part for file resolution
        url_no_anchor = url.split("#", 1)[0].split("?", 1)[0]
        if not url_no_anchor:
            continue
        # Skip absolute paths (these work on the deployed site, not local)
        if url_no_anchor.startswith("/"):
            continue
        # Decode %xx
        url_no_anchor = unquote(url_no_anchor)
        # Resolve relative to base_dir
        target = os.path.normpath(os.path.join(base_dir, url_no_anchor))
        if not os.path.exists(target):
            broken.append((url, target.replace(ROOT, "<site>")))
    return broken

total_files = 0
total_broken = 0
files_with_broken = 0
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".html"):
            continue
        total_files += 1
        path = os.path.join(root, f)
        broken = check_file_links(path)
        if broken:
            files_with_broken += 1
            total_broken += len(broken)
            rel = os.path.relpath(path, ROOT)
            print(f"\n{rel}  ({len(broken)} broken):")
            for url, tgt in broken[:10]:
                print(f"  -> {url}")
                print(f"     (resolves to {tgt})")
            if len(broken) > 10:
                print(f"  ... and {len(broken) - 10} more")

print(f"\n=== SUMMARY ===")
print(f"Total HTML files: {total_files}")
print(f"Files with broken links: {files_with_broken}")
print(f"Total broken links: {total_broken}")
