#!/usr/bin/env python3
"""
Fix the JSON lesson structure by:
1. Extracting proper lesson titles from PDFs
2. Reorganizing fragmented content blocks into coherent paragraphs
3. Removing page numbers and artifacts
"""

import json
import re
import pdfplumber
from pathlib import Path

def extract_lesson_titles_from_pdf(pdf_path):
    """Extract lesson titles from PDF table of contents."""
    titles = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Usually TOC is in first 5 pages
            for page_num in range(min(5, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    # Look for lesson patterns like "Lesson 1: Title" or "Lesson 1 – Title"
                    lesson_matches = re.findall(r'Lesson\s+(\d+)[:\s–-]+([^\n]+)', text, re.IGNORECASE)
                    for match in lesson_matches:
                        titles.append(match[1].strip())
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return titles

def reorganize_content_blocks(blocks):
    """Group fragmented paragraph blocks into coherent paragraphs."""
    organized = []
    i = 0

    while i < len(blocks):
        block = blocks[i]

        # If it's not a paragraph, add as-is
        if block.get('t') != 'p':
            organized.append(block)
            i += 1
            continue

        # Collect consecutive paragraphs that look like fragments
        paragraph_text = block.get('x', '')
        i += 1

        # If paragraph ends with punctuation or is long, it's complete
        ends_with_punct = paragraph_text.rstrip().endswith(('.', '!', '?', ':', '"', "'"))
        is_long = len(paragraph_text) > 150

        if ends_with_punct or is_long:
            organized.append({'t': 'p', 'x': paragraph_text})
            continue

        # Otherwise, collect consecutive fragments
        while i < len(blocks) and blocks[i].get('t') == 'p':
            next_text = blocks[i].get('x', '')
            if next_text and next_text[0].islower():
                paragraph_text += ' ' + next_text
                i += 1
                if paragraph_text.rstrip().endswith(('.', '!', '?', ':', '"', "'")):
                    break
            else:
                break

        if paragraph_text.strip():
            organized.append({'t': 'p', 'x': paragraph_text})

    return organized

def is_page_number_or_artifact(text):
    """Check if text is a page number or book artifact."""
    # Page number pattern: "123 ● Book Title" or similar
    if re.match(r'^\d+\s*●', text):
        return True
    # Pure page numbers
    if re.match(r'^\d+$', text.strip()):
        return True
    # Common footer patterns
    if any(x in text.lower() for x in ['table of contents', 'copyright', '© ', 'page']):
        return True
    return False

def clean_title(title):
    """Remove page numbers and dots from TOC-style titles."""
    # Remove trailing page numbers: "Title .................. 35" -> "Title"
    title = re.sub(r'\s*\.+\s*\d+\s*$', '', title)
    # Remove leading "Lesson N: " if present
    title = re.sub(r'^Lesson\s+\d+:\s*', '', title, flags=re.IGNORECASE)
    return title.strip()

def fix_json_file(json_path, pdf_path=None, lesson_titles=None):
    """Fix a JSON file by cleaning up lesson structure."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get lesson titles from PDF if available
    if pdf_path and not lesson_titles:
        lesson_titles = extract_lesson_titles_from_pdf(pdf_path)
        lesson_titles = [clean_title(t) for t in lesson_titles]

    # Fix each lesson
    for lesson_idx, lesson in enumerate(data.get('lessons', [])):
        # Fix lesson title
        if lesson.get('num', '').startswith('<!--'):
            lesson['num'] = f"{lesson_idx + 1}"

        if lesson.get('title', '').startswith('<!--'):
            if lesson_titles and lesson_idx < len(lesson_titles):
                lesson['title'] = lesson_titles[lesson_idx]
            else:
                # Fallback: use first non-artifact block or generic title
                lesson['title'] = f"Lesson {lesson_idx + 1}"
        else:
            # Clean up existing titles (remove page numbers and dots)
            lesson['title'] = clean_title(lesson['title'])

        # Clean blocks: remove artifacts and reorganize
        blocks = lesson.get('blocks', [])
        cleaned_blocks = [
            b for b in blocks
            if not is_page_number_or_artifact(b.get('x', ''))
        ]

        # Reorganize fragmented paragraphs
        cleaned_blocks = reorganize_content_blocks(cleaned_blocks)

        lesson['blocks'] = cleaned_blocks

    # Write back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ Fixed {json_path}")

if __name__ == '__main__':
    # Map JSON files to their source PDFs
    files_to_fix = [
        ('data/d1_final.json', 'input/121 PHILS TEXT.pdf'),
        ('data/cl_final.json', 'input/CL TEXT PHILS.pdf'),
        ('data/gal_final.json', 'input/GALATIANS PHILS TEXT.pdf'),
    ]

    for json_file, pdf_file in files_to_fix:
        if Path(json_file).exists():
            print(f"Fixing {json_file}...")
            fix_json_file(json_file, pdf_file)

    # Regenerate combined file
    print("\nRegenerating combined courses file...")
    all_courses = []
    for json_file in ['data/d1_final.json', 'data/cl_final.json', 'data/gal_final.json']:
        if Path(json_file).exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                all_courses.append(json.load(f))

    with open('data/courses_final.json', 'w', encoding='utf-8') as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=2)

    # Copy to public folder
    import shutil
    shutil.copy('data/courses_final.json', 'public/data/courses.json')
    print("✓ Copied to public/data/courses.json")
    print("\n✅ All JSON files fixed!")
