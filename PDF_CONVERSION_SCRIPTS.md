# PDF to Markdown Conversion Scripts

This document contains the scripts used to convert the course PDFs to markdown format.

## Script 1: Extract PDF text to raw markdown

**Purpose**: Convert PDF files to markdown format, preserving all text content

**Tool**: Python with `pdfplumber` library

```python
import pdfplumber
import os

# Define PDF files and output names
pdfs = [
    ('C:/Users/viren/source/jcbiblecourse/121 PHILS TEXT.pdf', 'C:/Users/viren/source/jcbiblecourse/121-PHILS-TEXT.md'),
    ('C:/Users/viren/source/jcbiblecourse/CL TEXT PHILS.pdf', 'C:/Users/viren/source/jcbiblecourse/CL-TEXT-PHILS.md'),
    ('C:/Users/viren/source/jcbiblecourse/GALATIANS PHILS TEXT.pdf', 'C:/Users/viren/source/jcbiblecourse/GALATIANS-PHILS-TEXT.md')
]

for pdf_path, md_path in pdfs:
    print(f'Converting {os.path.basename(pdf_path)}...')
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append(f'\n<!-- Page {i+1} -->\n{text}')
        
        # Join all pages
        full_text = '\n'.join(all_text)
        
        # Write to markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f'  ✓ Saved to {os.path.basename(md_path)}')

print('\nConversion complete!')
```

**Output**: Raw markdown files with all text preserved, page breaks marked with HTML comments

---

## Script 2: Reformat markdown with proper structure

**Purpose**: Add markdown headers, emphasis, and structure to improve readability

**File**: `reformat_markdown.py` (created in project directory)

**Key transformations**:
- `# ` for main titles
- `## ` for units/major sections
- `### ` for lessons/encounters
- `#### ` for section labels (A., B., C., etc.)
- `**bold**` for emphasis and subsection numbers
- `> **Question**` for question formatting
- Removes copyright boilerplate and page markers
- Organizes hierarchical structure

**Usage**:
```bash
cd C:\Users\viren\source\jcbiblecourse
python reformat_markdown.py
```

---

## Prerequisites

Install pdfplumber:
```bash
pip install pdfplumber
```

---

## Output Files

| File | Size | Pages | Content |
|------|------|-------|---------|
| 121-PHILS-TEXT.md | 159.5 KB | 133 | One-to-One Discipleship Training |
| CL-TEXT-PHILS.md | 207.5 KB | 180 | Christian Life |
| GALATIANS-PHILS-TEXT.md | 129.75 KB | 115 | Galatians Study |

---

## Notes

- All text content is preserved during conversion
- Markdown formatting makes the files easier to read and search
- Files are ready to be used as source material for Gemini Notebook prompts
- Page markers preserved in comments for reference
