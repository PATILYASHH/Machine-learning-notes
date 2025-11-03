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

# Mapping of question files to their details
QUESTION_MAP = {
    # Unit 1 - 4 marks
    '4Q1.md': ('Explain different phases of predictive modeling (8 phases)', 'Unit 1', '4 marks'),
    '4Q2.md': ('Advantages and Disadvantages of K-nearest neighbor algorithm', 'Unit 1', '4 marks'),
    '4Q3.md': ('Define Machine Learning and explain features of machine learning', 'Unit 1', '4 marks'),
    
    # Unit 1 - 8 marks
    'Q4.md': ('Explain Difference between Artificial Intelligence and Machine learning', 'Unit 1', '8 marks'),
    'Q5.md': ('Explain Development steps in Machine Learning', 'Unit 1', '8 marks'),
    'Q6.md': ('Explain K-nearest neighbor algorithm in detail', 'Unit 1', '8 marks'),
    
    # Unit 2 - 4 marks
    'Q7.md': ('State the goals of Machine Learning', 'Unit 2', '4 marks'),
    'Q8.md': ('Write a note on speech Recognition and production recommendations', 'Unit 2', '4 marks'),
    'Q9.md': ('Advantages and Disadvantages of machine learning', 'Unit 2', '4 marks'),
    'Q10.md': ('Write a note on function approximation', 'Unit 2', '4 marks'),
    
    # Unit 2 - 8 marks
    'Q11.md': ('Explain in detail the application of Machine learning', 'Unit 2', '8 marks'),
    'Q12.md': ('What is the need for ML? Explain in detail classification of ML', 'Unit 2', '8 marks'),
    'Q13.md': ('Explain steps to design a learning system', 'Unit 2', '8 marks'),
    
    # Unit 3 - 4 marks
    'Q14.md': ('Explain bias and variance with example', 'Unit 3', '4 marks'),
    'Q15.md': ('Write a short note on confusion matrix', 'Unit 3', '4 marks'),
    'Q16.md': ('How to treat data in ML', 'Unit 3', '4 marks'),
    'Q17.md': ('What is Data pre-processing? Why do we need it?', 'Unit 3', '4 marks'),
    'Q18.md': ('Explain performance measures of ML', 'Unit 3', '4 marks'),
    'Q19.md': ('Write a note on bootstrap sampling', 'Unit 3', '4 marks'),
    'Q20.md': ('Difference between bagging and boosting', 'Unit 3', '4 marks'),
    'Q21.md': ('Write a note on bagging aggregation', 'Unit 3', '4 marks'),
    
    # Unit 3 - 8 marks
    'Q22.md': ('Explain in detail types of ML', 'Unit 3', '8 marks'),
    'Q23.md': ('What is bias and variance? Explain in detail', 'Unit 3', '8 marks'),
    'Q24.md': ('What is bias and variance and what is Bias-variance tradeoff?', 'Unit 3', '8 marks'),
    'Q25.md': ('Explain overfitting and underfitting in ML', 'Unit 3', '8 marks'),
    
    # Unit 4
    'Q26.md': ('State and prove Bayes theorem with example', 'Unit 4', '8 marks'),
    'Q27.md': ('What is probability? What are the rules of probability', 'Unit 4', '8 marks'),
    'Q28.md': ('Difference between permutation and combination', 'Unit 4', '4 marks'),
}


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

    md_files = sorted([p for p in ROOT.glob("*.md") if p.name != "README.MD"])
    if not md_files:
        print("No markdown files found in the repository root.")
        return

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        
        # Get question details from map or extract from content
        if md.name in QUESTION_MAP:
            title, unit, marks = QUESTION_MAP[md.name]
        else:
            title = title_from_md(text, md.stem)
            unit = "General"
            marks = ""
        
        html_body = markdown.markdown(
            text,
            extensions=["fenced_code", "codehilite", "toc", "tables"],
            output_format="html5",
        )
        slug = slug_from_path(md)
        pages.append({
            "title": title,
            "slug": slug,
            "src": md.name,
            "unit": unit,
            "marks": marks
        })

        # Add back button, TTS button and bookmark button to content
        back_btn = '<a href="index.html" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Questions</a>'
        tts_btn = '<button class="tts-btn" id="ttsBtn" title="Read aloud"><i class="fas fa-volume-up"></i> <span>Read Aloud</span></button>'
        bookmark_btn = f'<button class="page-bookmark-btn" id="pageBookmarkBtn" data-slug="{slug}" data-title="{title}" title="Bookmark this question"><i class="far fa-bookmark"></i></button>'
        
        # Wrap the answer content in a div for TTS to target
        answer_content = f'<div id="answerContent" class="answer-content">{html_body}</div>'
        
        full_content = back_btn + tts_btn + answer_content + bookmark_btn

        # render page
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        page_html = base.replace("{title}", title).replace("{content}", full_content)

        (OUT / slug).write_text(page_html, encoding="utf-8")
        print(f"Wrote {slug}")

    # Generate index with modern UI
    generate_index(pages)

    print(f"Site generated in: {OUT}")


def generate_index(pages):
    """Generate a modern index page with search, filter, and question cards"""
    
    # Group questions by unit
    units = {}
    for page in pages:
        unit = page['unit']
        if unit not in units:
            units[unit] = []
        units[unit].append(page)
    
    # Create search and filter UI
    search_html = '''
    <div class="search-container">
        <i class="fas fa-search search-icon"></i>
        <input type="text" id="searchInput" class="search-input" placeholder="Search questions...">
    </div>
    
    <div class="filter-tabs">
        <button class="filter-tab active" data-filter="all">All Questions</button>
        <button class="filter-tab" data-filter="Unit 1"><i class="fas fa-book"></i> Unit 1</button>
        <button class="filter-tab" data-filter="Unit 2"><i class="fas fa-book"></i> Unit 2</button>
        <button class="filter-tab" data-filter="Unit 3"><i class="fas fa-book"></i> Unit 3</button>
        <button class="filter-tab" data-filter="Unit 4"><i class="fas fa-book"></i> Unit 4</button>
    </div>
    '''
    
    # Create question cards
    cards_html = '<div class="questions-grid">'
    question_number = 1
    
    for unit_name in sorted(units.keys()):
        for page in units[unit_name]:
            marks_badge = f" • {page['marks']}" if page['marks'] else ""
            cards_html += f'''
            <div class="question-card" data-unit="{page['unit']}" onclick="window.location.href='{page['slug']}'">
                <div class="question-number">Q{question_number}</div>
                <div class="question-title">{page['title']}</div>
                <div class="question-footer">
                    <span class="question-unit"><i class="fas fa-tag"></i> {page['unit']}{marks_badge}</span>
                    <button class="bookmark-btn" data-slug="{page['slug']}" data-title="{page['title']}" onclick="event.stopPropagation()">
                        <i class="far fa-bookmark"></i>
                    </button>
                </div>
            </div>
            '''
            question_number += 1
    
    cards_html += '</div>'
    
    # Combine everything
    index_content = f'''
    <div class="hero-section">
        <h1><i class="fas fa-graduation-cap"></i> Machine Learning Notes</h1>
        <p style="color: var(--muted); font-size: 1.1rem; margin-bottom: 0;">Comprehensive study material with {len(pages)} questions across 4 units</p>
    </div>
    {search_html}
    {cards_html}
    '''
    
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    index_html = base.replace("{title}", "Machine Learning Notes").replace("{content}", index_content)
    (OUT / "index.html").write_text(index_html, encoding="utf-8")
    print("Generated index.html with modern UI")


if __name__ == "__main__":
    build()

