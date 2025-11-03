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
import json

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


def parse_readme_structure():
    """Parse README.MD to extract question organization by units."""
    readme_path = ROOT / "README.MD"
    if not readme_path.exists():
        return {}
    
    text = readme_path.read_text(encoding="utf-8")
    units = {}
    current_unit = None
    current_marks = None
    
    for line in text.split("\n"):
        # Match unit headers like "# *UNIT 1*"
        unit_match = re.match(r"#\s*\*?UNIT\s+(\d+)\*?", line, re.IGNORECASE)
        if unit_match:
            unit_num = int(unit_match.group(1))
            current_unit = f"Unit {unit_num}"
            if current_unit not in units:
                units[current_unit] = {"4-marks": [], "8-marks": []}
            continue
        
        # Match marks headers like "### Unit 1 - 4 marks"
        marks_match = re.match(r"###\s*Unit\s+\d+\s*-\s*(\d+)\s*marks?", line, re.IGNORECASE)
        if marks_match and current_unit:
            marks = marks_match.group(1)
            current_marks = f"{marks}-marks"
            continue
        
        # Match question lines like "Q. ... [Click Here](Q5.md)"
        q_match = re.search(r"Q\.?\s+(.+?)\s*\[Click Here\]\(([^)]+)\)", line, re.IGNORECASE)
        if q_match and current_unit and current_marks:
            question_text = q_match.group(1).strip()
            file_name = q_match.group(2).strip()
            units[current_unit][current_marks].append({
                "text": question_text,
                "file": file_name
            })
    
    return units


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # copy static
    if STATIC_SRC.exists():
        shutil.copytree(STATIC_SRC, OUT / "static")

    pages = []
    
    # Parse README structure
    units_structure = parse_readme_structure()

    md_files = sorted([p for p in ROOT.glob("*.md") if p.name != "README.MD"])
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

        # render page with question template
        base = (TEMPLATES / "question.html").read_text(encoding="utf-8")
        page_html = base.replace("{title}", title).replace("{content}", html_body)

        (OUT / slug).write_text(page_html, encoding="utf-8")
        print(f"Wrote {slug}")

    # Create a JSON file with questions data for JavaScript
    questions_data = []
    for unit_name, marks_data in units_structure.items():
        for marks, questions in marks_data.items():
            for q in questions:
                slug = q["file"].replace(".md", ".html")
                # Find the title from pages
                page_title = None
                for p in pages:
                    if p["src"] == q["file"]:
                        page_title = p["title"]
                        break
                if not page_title:
                    page_title = q["text"]
                
                questions_data.append({
                    "unit": unit_name,
                    "marks": marks,
                    "text": q["text"],
                    "title": page_title,
                    "slug": slug
                })
    
    # Write questions data as JSON
    (OUT / "questions.json").write_text(json.dumps(questions_data, indent=2), encoding="utf-8")

    # generate index with new template
    index_template = (TEMPLATES / "index.html").read_text(encoding="utf-8")
    (OUT / "index.html").write_text(index_template, encoding="utf-8")

    print(f"Site generated in: {OUT}")


if __name__ == "__main__":
    build()
