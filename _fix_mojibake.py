"""
Rename mojibake folder names in docs/ from ΓÇö -> — (em dash, U+2014)
and update all .md files in docs/ to use — instead of ΓÇö and Γçö in their
content (both in href attributes and in display text).

Also updates the inner .md front matter titles if they contain the mojibake.
"""
import os
import re
from pathlib import Path

DOCS = Path(r"C:\Users\Henry\Documents\Github\tenniskb\docs")
EM = "\u2014"  # em dash —

# 1) Rename folders: ΓÇö -> —
folders_renamed = []
for d in sorted(DOCS.rglob("*"), reverse=True):  # reverse so deepest first
    if d.is_dir() and "ΓÇö" in d.name:
        new_name = d.name.replace("ΓÇö", EM)
        new_path = d.parent / new_name
        print(f"RENAME FOLDER: {d} -> {new_path}")
        d.rename(new_path)
        folders_renamed.append((str(d), str(new_path)))

# 2) Update .md content: ΓÇö -> — and Γçö -> —
files_updated = []
for md in DOCS.rglob("*.md"):
    with open(md, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content
    # Replace both forms of the mojibake em-dash
    new_content = new_content.replace("ΓÇö", EM)
    new_content = new_content.replace("Γçö", EM)
    if new_content != content:
        with open(md, "w", encoding="utf-8") as f:
            f.write(new_content)
        files_updated.append(str(md))
        print(f"UPDATED MD: {md}")

print(f"\nFolders renamed: {len(folders_renamed)}")
print(f"Files updated: {len(files_updated)}")
