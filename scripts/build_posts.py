#!/usr/bin/env python3
"""Convert any new .docx in blog_files/ into Jekyll posts under _posts/.

Tracks processed files in blog_files/index.json so re-runs only handle
new docx files. Run from anywhere:
    python3 scripts/build_posts.py
"""
import json
import re
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO / "blog_files"
POSTS_DIR = REPO / "_posts"
INDEX_FILE = BLOG_DIR / "index.json"

MONTHS = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}

HEADER_PATTERNS = [
    r"^\*\*Autor:.*\*\*\s*$",
    r"^\*\*Académico.*\*\*\s*$",
    r"^\*\*Twitter:.*\*\*\s*$",
    r"^\*\*LinkedIn:.*\*\*\s*$",
    r"^\*\*Mail:.*\*\*\s*$",
]

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].strip("-")

def parse_date(stem):
    m = re.match(r"([A-Za-z]{3})(\d{1,2})(\d{4})$", stem)
    if not m:
        return None
    mon, day, year = m.group(1), m.group(2), m.group(3)
    if mon not in MONTHS:
        return None
    return f"{year}-{MONTHS[mon]}-{int(day):02d}"

def docx_to_md(docx):
    return subprocess.run(
        ["pandoc", str(docx), "-t", "markdown_strict", "--wrap=none"],
        check=True, capture_output=True, text=True,
    ).stdout

def extract_title_and_body(md):
    lines = [l for l in md.splitlines() if not any(re.match(p, l) for p in HEADER_PATTERNS)]
    title, title_idx = None, None
    for i, line in enumerate(lines):
        m = re.match(r"^\*\*Titulo:\s*(.+?)\s*\*\*\s*$", line)
        if m:
            title, title_idx = m.group(1).strip().rstrip("."), i
            break
    if title is None:
        for i, line in enumerate(lines):
            m = re.match(r"^\*\*Columna:\s*(.+?)\s*\*\*\s*$", line)
            if m:
                title, title_idx = m.group(1).strip().rstrip("."), i
                break
    if title is None:
        return None, None
    body = []
    for i, line in enumerate(lines):
        if i == title_idx:
            continue
        if re.match(r"^\*\*Columna:.*\*\*\s*$", line):
            continue
        body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return title, "\n".join(body)

def write_post(date, title, body):
    slug = slugify(title)
    out = POSTS_DIR / f"{date}-{slug}.md"
    safe_title = title.replace('"', '\\"')
    front = (
        "---\n"
        "layout: single\n"
        f'title: "{safe_title}"\n'
        "toc: False\n"
        "author_profile: True\n"
        "category: ['articulos']\n"
        "tags: ['mexico', 'financiero', 'spanish', 'ia']\n"
        "---\n\n"
    )
    out.write_text(front + body + "\n", encoding="utf-8")
    return out.name

def load_index():
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {"posts": {}}

def save_index(index):
    index["posts"] = dict(sorted(index["posts"].items()))
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")

def main():
    index = load_index()
    processed = index["posts"]
    new_count = 0
    for docx in sorted(BLOG_DIR.glob("*.docx")):
        if docx.name in processed:
            continue
        date = parse_date(docx.stem)
        if not date:
            print(f"skip {docx.name}: cannot parse date from filename")
            continue
        title, body = extract_title_and_body(docx_to_md(docx))
        if not title:
            print(f"skip {docx.name}: no title found")
            continue
        post_name = write_post(date, title, body)
        processed[docx.name] = {
            "post": post_name,
            "title": title,
            "date": date,
            "added": datetime.now().strftime("%Y-%m-%d"),
        }
        print(f"+ {docx.name} -> {post_name}")
        new_count += 1
    save_index(index)
    print(f"done: {new_count} new post(s), {len(processed)} total")

if __name__ == "__main__":
    main()
