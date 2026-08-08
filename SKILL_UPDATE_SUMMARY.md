# PDF-to-Markdown-Course Skill - Complete Pipeline Update

## ✓ UPDATED: Full End-to-End Automation

The skill now handles the **complete workflow** from PDF to structured JSON, requiring just one command.

### What the skill does (automatic, no configuration)

```
PDF Files
  ↓ [ONE COMMAND]
    1. Convert PDF → Markdown (with TOC, hierarchy preserved)
    2. Clean markdown (remove TOC, add content markers)
    3. Parse to JSON (extract lessons, questions, objectives)
  ↓
Final Output
  - Original markdown (with Table of Contents for reference)
  - Cleaned markdown (_PARSING.md)
  - Structured JSON with all lessons and questions
```

## How to use

### Setup (one-time)
```bash
pip install pdfplumber
```

### Place your PDFs
Create an `input/` folder and add your course PDFs:
```
your-project/
└── input/
    ├── Course-1.pdf
    ├── Course-2.pdf
    └── Course-3.pdf
```

### Run the skill
```
/pdf-to-markdown-course
```

That's it! The skill will:
- Convert all PDFs to markdown
- Clean up formatting automatically
- Extract all lessons, questions, and objectives to JSON
- Save everything to `output/` and `data/` folders

## Output files generated

### Markdown files (`output/` folder)
- **Course-1.md** — Original with Table of Contents (preserved for reference)
- **Course-1_PARSING.md** — Cleaned version (TOC removed, ready to parse)
- Similar files for each PDF

### JSON files (`data/` folder)
- **course1_final.json** — Structured course data with all lessons
- **course2_final.json**
- **courses_final.json** — Combined data for all courses

### JSON structure
Each course includes:
```json
{
  "id": "d1",
  "title": "Course Name",
  "lessons": [
    {
      "num": "Lesson 1: Title",
      "title": "Lesson 1: Title",
      "objectives": ["Learn X", "Understand Y"],
      "assignments": ["Read section", "Answer questions"],
      "blocks": [
        {"t": "h2", "x": "Section Header"},
        {"t": "q", "n": "1", "x": "Question text?"},
        {"t": "p", "x": "Paragraph of explanation..."}
      ],
      "qCount": 5
    }
  ]
}
```

## Key features

✓ **Fully automated** — One command handles all three steps
✓ **Content preservation** — Original markdown with TOC kept for reference  
✓ **Quality markers** — `<!--CONTENT START-->` shows where cleanup happened
✓ **Question extraction** — All questions in `> **Question N: text**` format extracted
✓ **Objective extraction** — Learning objectives and assignments parsed
✓ **Batch processing** — Handles multiple PDFs at once
✓ **No configuration** — Works out of the box

## Example workflow

```bash
# 1. Add PDFs to input folder
cp *.pdf input/

# 2. Run the skill (that's it!)
/pdf-to-markdown-course

# 3. Check output
ls output/     # Contains .md and _PARSING.md files
ls data/       # Contains JSON files ready for your application
```

## Technical details

**Skill location:** `pdf-to-markdown-course`

**Scripts included:**
- `pdf_to_markdown.py` — PDF extraction to markdown
- `cleanup_markdown.py` — TOC removal, normalization
- `parse_courses_v2.py` — JSON structure generation
- `run_pipeline.py` — Orchestrates all three steps

**Requirements:**
- Python 3.7+
- pdfplumber library

**Compatible with:**
- Discipleship training materials
- Bible study guides
- Educational textbooks
- Course materials with questions and objectives

## Next steps

Use the generated JSON in:
- Claude Design for web page rendering
- Learning management systems
- Educational applications
- Content databases
- Course delivery platforms
