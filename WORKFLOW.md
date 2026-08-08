# Course Content Processing Workflow

## The Three-Step Pipeline

```
PDF Files
    ↓
[pdf_to_markdown_course skill]
    ↓
Raw Markdown (with formatting issues)
    ↓
[Manual/Automated Cleanup]
    ↓
Clean Markdown (proper structure)
    ↓
[parse_courses_v2.py parser]
    ↓
Structured JSON (for Claude Design app)
```

## Step 1: PDF → Markdown

**Tool:** `pdf_to_markdown_course` skill
**Status:** ✅ Complete
**Input:** PDF files
**Output:** Raw markdown files in `output/`

Files created:
- `121 PHILS TEXT.md` (Discipleship Training) - 165 KB
- `CL TEXT PHILS.md` (Christian Life) - 215 KB
- `GALATIANS PHILS TEXT.md` (Galatians) - 134 KB

## Step 2: Cleanup Markdown

**Status:** ⏳ Needed
**What needs fixing:**

The extracted markdown has several issues:

1. **Formatting preservation**: Some headers got merged together
2. **Section markers**: "LESSON OUTLINE" and "LESSON OBJECTIVES" appear to be on same line
3. **Consistent markdown format**: Ensure all lessons follow same structure
4. **Remove artifacts**: PDf conversion may have left page breaks, headers, etc.

### Cleanup Checklist

For each markdown file:
- [ ] Open in text editor
- [ ] Search for "LESSON OUTLINE LESSON OBJECTIVES" - should be TWO separate lines
- [ ] Verify each lesson section has this structure:
  ```markdown
  ### Lesson Title: Subtitle
  LESSON OUTLINE
  (outline content)
  
  LESSON OBJECTIVES
  - Objective 1
  - Objective 2
  
  ASSIGNMENTS
  - Assignment 1
  - Assignment 2
  
  LESSON DEVELOPMENT
  (content with subsections and questions)
  ```
- [ ] Ensure questions are formatted consistently
- [ ] Remove page numbers and headers/footers if present

## Step 3: Parser → JSON

**Tool:** `parse_courses_v2.py`
**Status:** ⚠️ In progress (structure right, content parsing needs work)
**Input:** Clean markdown files
**Output:** Structured JSON

```bash
python parse_courses_v2.py
# Generates: courses_final.json + individual course files
```

### Parser Output Structure

Each course should have:
- 15 lessons (Discipleship) with proper objectives/assignments/content
- All questions extracted and numbered
- Units properly organized (Unit I, II, III)

Current issue: Content blocks are empty - the section parsing needs debugging.

## Files in This Repo

```
jcbiblecourse/
├── output/                    # Raw markdown from PDF conversion
│   ├── 121 PHILS TEXT.md
│   ├── CL TEXT PHILS.md
│   └── GALATIANS PHILS TEXT.md
├── parse_courses.py          # v1 parser (basic approach)
├── parse_courses_v2.py       # v2 parser (better structure, incomplete)
├── courses_final.json        # Output from v2 (needs content)
├── data/
│   ├── d1_final.json        # Discipleship course
│   ├── cl_final.json        # Christian Life course
│   └── gal_final.json       # Galatians course
├── WORKFLOW.md              # This file
└── PARSER_README.md         # Parser documentation
```

## Next Actions

1. **Manually review one lesson** in the markdown to identify cleanup needs
2. **Fix section extraction** in the parser (debug why sections aren't being found)
3. **Run parser again** on cleaned markdown
4. **Validate output** - spot check a few lessons to ensure structure is correct
5. **Import into Claude Design** app once parser works

## Alternative: Simplified Structure

If the parser proves too complex to fix, consider a **simpler hand-crafted structure**:
- Create course.json manually for ONE lesson
- Show it working in the Claude Design app
- Then batch-create the rest with a simpler script

This guarantees working content, even if not fully automated.
