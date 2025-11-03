#!/usr/bin/env python3
"""Simple static site generator for Markdown notes (project-local copy).

Usage:
  python3 build.py

This script finds all .md files at the repository root, converts them to HTML,
and writes them to the `site/` directory along with a generated index.html and
static assets.
"""
import re
import shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent.resolve()
OUT = ROOT / "site"
STATIC_SRC = ROOT / "static"
TEMPLATES = ROOT / "templates"


def title_from_md(text, default):
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # fallback to filename-like default
    return default


def slug_from_path(path: Path):
    return path.stem + ".html"


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # copy static
    if STATIC_SRC.exists():
        shutil.copytree(STATIC_SRC, OUT / "static")

    pages = []

    md_files = sorted([p for p in ROOT.glob("*.md")])
    if not md_files:
        print("No markdown files found in the repository root.")
        return

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        title = title_from_md(text, md.stem)
        html_body = markdown.markdown(
            text,
            extensions=["fenced_code", "codehilite", "toc"],
            output_format="html5",
        )
        slug = slug_from_path(md)
        pages.append({"title": title, "slug": slug, "src": md.name})

        # render page
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        page_html = base.replace("{title}", title).replace("{content}", html_body)

        (OUT / slug).write_text(page_html, encoding="utf-8")
        print(f"Wrote {slug}")

    # generate index
    index_items = []
    for p in pages:
        index_items.append(f"<li><a href=\"{p['slug']}\">{p['title']}</a> <small>({p['src']})</small></li>")
    index_content = "<h2>Notes</h2>\n<ul>" + "\n".join(index_items) + "</ul>\n"
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    index_html = base.replace("{title}", "Notes Index").replace("{content}", index_content)
    (OUT / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Site generated in: {OUT}")


if __name__ == "__main__":
    build()
