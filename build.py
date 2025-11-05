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

# Mapping of question files to their details (title, unit, marks, subject)
QUESTION_MAP = {
    # Machine Learning - Unit 1 - 4 marks
    '4Q1.md': ('Explain different phases of predictive modeling (8 phases)', 'Unit 1', '4 marks', 'ML'),
    '4Q2.md': ('Advantages and Disadvantages of K-nearest neighbor algorithm', 'Unit 1', '4 marks', 'ML'),
    '4Q3.md': ('Define Machine Learning and explain features of machine learning', 'Unit 1', '4 marks', 'ML'),
    
    # Machine Learning - Unit 1 - 8 marks
    'Q4.md': ('Explain Difference between Artificial Intelligence and Machine learning', 'Unit 1', '8 marks', 'ML'),
    'Q5.md': ('Explain Development steps in Machine Learning', 'Unit 1', '8 marks', 'ML'),
    'Q6.md': ('Explain K-nearest neighbor algorithm in detail', 'Unit 1', '8 marks', 'ML'),
    
    # Machine Learning - Unit 2 - 4 marks
    'Q7.md': ('State the goals of Machine Learning', 'Unit 2', '4 marks', 'ML'),
    'Q8.md': ('Write a note on speech Recognition and production recommendations', 'Unit 2', '4 marks', 'ML'),
    'Q9.md': ('Advantages and Disadvantages of machine learning', 'Unit 2', '4 marks', 'ML'),
    'Q10.md': ('Write a note on function approximation', 'Unit 2', '4 marks', 'ML'),
    
    # Machine Learning - Unit 2 - 8 marks
    'Q11.md': ('Explain in detail the application of Machine learning', 'Unit 2', '8 marks', 'ML'),
    'Q12.md': ('What is the need for ML? Explain in detail classification of ML', 'Unit 2', '8 marks', 'ML'),
    'Q13.md': ('Explain steps to design a learning system', 'Unit 2', '8 marks', 'ML'),
    
    # Machine Learning - Unit 3 - 4 marks
    'Q14.md': ('Explain bias and variance with example', 'Unit 3', '4 marks', 'ML'),
    'Q15.md': ('Write a short note on confusion matrix', 'Unit 3', '4 marks', 'ML'),
    'Q16.md': ('How to treat data in ML', 'Unit 3', '4 marks', 'ML'),
    'Q17.md': ('What is Data pre-processing? Why do we need it?', 'Unit 3', '4 marks', 'ML'),
    'Q18.md': ('Explain performance measures of ML', 'Unit 3', '4 marks', 'ML'),
    'Q19.md': ('Write a note on bootstrap sampling', 'Unit 3', '4 marks', 'ML'),
    'Q20.md': ('Difference between bagging and boosting', 'Unit 3', '4 marks', 'ML'),
    'Q21.md': ('Write a note on bagging aggregation', 'Unit 3', '4 marks', 'ML'),
    
    # Machine Learning - Unit 3 - 8 marks
    'Q22.md': ('Explain in detail types of ML', 'Unit 3', '8 marks', 'ML'),
    'Q23.md': ('What is bias and variance? Explain in detail', 'Unit 3', '8 marks', 'ML'),
    'Q24.md': ('What is bias and variance and what is Bias-variance tradeoff?', 'Unit 3', '8 marks', 'ML'),
    'Q25.md': ('Explain overfitting and underfitting in ML', 'Unit 3', '8 marks', 'ML'),
    
    # Machine Learning - Unit 4
    'Q26.md': ('State and prove Bayes theorem with example', 'Unit 4', '8 marks', 'ML'),
    'Q27.md': ('What is probability? What are the rules of probability', 'Unit 4', '8 marks', 'ML'),
    'Q28.md': ('Difference between permutation and combination', 'Unit 4', '4 marks', 'ML'),
    
    # Java - Unit 1
    'j1.md': ('Write a short note on Features of Java', 'Unit 1', '4 marks', 'JAVA'),
    'j2.md': ('Write a short note on JVM', 'Unit 1', '4 marks', 'JAVA'),
    'j3.md': ('Describe primitive data types in Java', 'Unit 1', '4 marks', 'JAVA'),
    'j4.md': ('Write a short note on Type Casting in Java', 'Unit 1', '4 marks', 'JAVA'),
    'j5.md': ('Explain compilation and execution process of a Java program', 'Unit 1', '4 marks', 'JAVA'),
    'j6.md': ('Describe break and continue statements in Java', 'Unit 1', '4 marks', 'JAVA'),
    'j7.md': ('Explain any four operators in Java with example', 'Unit 1', '8 marks', 'JAVA'),
    'j8.md': ('Explain looping statements in Java with example', 'Unit 1', '8 marks', 'JAVA'),
    'j9.md': ('Explain branching statements in Java with example', 'Unit 1', '8 marks', 'JAVA'),
    'j10.md': ('What is type casting? Explain implicit and explicit type casting with example', 'Unit 1', '8 marks', 'JAVA'),
    
    # Java
    'java.md': ('Write a short note on features of Java', 'General', '', 'JAVA'),
    
    # C#
    'csharp.md': ('C# Questions', 'General', '', 'C#'),
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
            title, unit, marks, subject = QUESTION_MAP[md.name]
        else:
            title = title_from_md(text, md.stem)
            unit = "General"
            marks = ""
            subject = "General"
        
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
            "marks": marks,
            "subject": subject
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
    """Generate a landing page with subject selection cards"""
    
    # Count questions by subject
    subject_counts = {}
    for page in pages:
        subject = page['subject']
        if subject not in subject_counts:
            subject_counts[subject] = 0
        subject_counts[subject] += 1
    
    # Define the three main subjects with icons and descriptions
    main_subjects = [
        {
            'name': 'ML',
            'full_name': 'Machine Learning',
            'icon': 'fa-brain',
            'description': 'Comprehensive ML study material covering all units',
            'color': '#7dd3fc',
            'count': subject_counts.get('ML', 0)
        },
        {
            'name': 'JAVA',
            'full_name': 'Java Programming',
            'icon': 'fa-coffee',
            'description': 'Java programming questions and concepts',
            'color': '#f59e0b',
            'count': subject_counts.get('JAVA', 0)
        },
        {
            'name': 'C#',
            'full_name': 'C# Programming',
            'icon': 'fa-code',
            'description': 'C# programming questions and concepts',
            'color': '#10b981',
            'count': subject_counts.get('C#', 0)
        }
    ]
    
    # Create subject selection cards
    subject_cards = ''
    for subject in main_subjects:
        subject_cards += f'''
        <div class="subject-card" onclick="window.location.href='subject-{subject['name'].lower().replace('#', 'sharp')}.html'" style="--card-color: {subject['color']}">
            <div class="subject-icon">
                <i class="fas {subject['icon']}"></i>
            </div>
            <h2 class="subject-title">{subject['full_name']}</h2>
            <p class="subject-description">{subject['description']}</p>
            <div class="subject-count">{subject['count']} Questions</div>
            <div class="subject-action">
                <span>View Questions</span>
                <i class="fas fa-arrow-right"></i>
            </div>
        </div>
        '''
    
    # Combine everything for landing page
    index_content = f'''
    <div class="hero-section">
        <h1><i class="fas fa-graduation-cap"></i> Study Notes</h1>
        <p style="color: var(--muted); font-size: 1.1rem; margin-bottom: 0;">Select a subject to start learning</p>
    </div>
    
    <div class="subject-selection-grid">
        {subject_cards}
    </div>
    '''
    
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    index_html = base.replace("{title}", "Study Notes - Select Subject").replace("{content}", index_content)
    (OUT / "index.html").write_text(index_html, encoding="utf-8")
    print("Generated index.html with subject selection cards")
    
    # Generate individual subject pages
    generate_subject_pages(pages, main_subjects)


def generate_subject_pages(pages, main_subjects):
    """Generate individual pages for each subject with questions"""
    
    for subject_info in main_subjects:
        subject_name = subject_info['name']
        subject_full = subject_info['full_name']
        
        # Filter pages for this subject
        subject_pages = [p for p in pages if p['subject'] == subject_name]
        
        if not subject_pages:
            continue
        
        # Group by unit
        units = {}
        for page in subject_pages:
            unit = page['unit']
            if unit not in units:
                units[unit] = []
            units[unit].append(page)
        
        # Create search and filter UI
        search_html = f'''
        <div class="search-container">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="searchInput" class="search-input" placeholder="Search questions...">
        </div>
        
        <div class="filter-section">
            <div class="filter-label">Filter by Unit:</div>
            <div class="filter-tabs unit-tabs">
                <button class="filter-tab active" data-filter="all-units">All Units</button>
                <button class="filter-tab" data-filter="Unit 1"><i class="fas fa-book"></i> Unit 1</button>
                <button class="filter-tab" data-filter="Unit 2"><i class="fas fa-book"></i> Unit 2</button>
                <button class="filter-tab" data-filter="Unit 3"><i class="fas fa-book"></i> Unit 3</button>
                <button class="filter-tab" data-filter="Unit 4"><i class="fas fa-book"></i> Unit 4</button>
            </div>
        </div>
        '''
        
        # Create question cards
        cards_html = '<div class="questions-grid">'
        question_number = 1
        
        for unit_name in sorted(units.keys()):
            for page in units[unit_name]:
                marks_badge = f" • {page['marks']}" if page['marks'] else ""
                unit = page['unit']
                
                # Avoid duplicate labels when subject and unit are the same
                if subject_name == unit:
                    badge_text = unit + marks_badge
                else:
                    badge_text = f"{unit}{marks_badge}"
                
                cards_html += f'''
                <div class="question-card" data-unit="{page['unit']}" data-subject="{page['subject']}" onclick="window.location.href='{page['slug']}'">
                    <div class="question-number">Q{question_number}</div>
                    <div class="question-title">{page['title']}</div>
                    <div class="question-footer">
                        <span class="question-unit"><i class="fas fa-tag"></i> {badge_text}</span>
                        <button class="bookmark-btn" data-slug="{page['slug']}" data-title="{page['title']}" onclick="event.stopPropagation()">
                            <i class="far fa-bookmark"></i>
                        </button>
                    </div>
                </div>
                '''
                question_number += 1
        
        cards_html += '</div>'
        
        # Back button to return to subject selection
        back_button = '<a href="index.html" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Subjects</a>'
        
        # Combine everything
        subject_content = f'''
        {back_button}
        <div class="hero-section">
            <h1><i class="fas {subject_info['icon']}"></i> {subject_full}</h1>
            <p style="color: var(--muted); font-size: 1.1rem; margin-bottom: 0;">{len(subject_pages)} questions available</p>
        </div>
        {search_html}
        {cards_html}
        '''
        
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        subject_html = base.replace("{title}", f"{subject_full} - Study Notes").replace("{content}", subject_content)
        
        # Write subject page
        filename = f"subject-{subject_name.lower().replace('#', 'sharp')}.html"
        (OUT / filename).write_text(subject_html, encoding="utf-8")
        print(f"Generated {filename}")


if __name__ == "__main__":
    build()

