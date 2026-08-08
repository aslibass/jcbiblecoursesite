# Markdown Processing Workflow

## File Organization

Each course has THREE versions:

### 1. **Original with TOC** (Reference & Verification)
```
output/121 PHILS TEXT.md          (Original from PDF conversion with Table of Contents)
output/CL TEXT PHILS.md           (Original with TOC)
output/GALATIANS PHILS TEXT.md    (Original with TOC)
```
- **Purpose**: Reference - shows what lessons SHOULD be there
- **Keep**: Yes, forever
- **When to use**: To verify parser didn't miss lessons

### 2. **Cleaned for Parsing** (Processing)
```
output/121 PHILS TEXT_PARSING.md  (Cleaned: no TOC, normalized sections)
output/CL TEXT PHILS_PARSING.md   (Cleaned: no TOC, normalized sections)
output/GALATIANS PHILS TEXT_PARSING.md
```
- **Purpose**: Input to parser - simplified structure
- **Keep**: Yes, regenerate as needed
- **When to use**: Feed to parse_courses.py

### 3. **Final JSON Output** (Result)
```
data/d1_final.json                (Structured course data)
data/cl_final.json
data/gal_final.json
```
- **Purpose**: Ready for Claude Design app
- **Keep**: Yes
- **When to use**: Import into Course Site application

## Processing Pipeline

```
Original.md (with TOC)
    ↓
[cleanup_markdown.py with --preserve-toc flag]
    ↓
Original.md (untouched)  +  _PARSING.md (cleaned)
    ↓ (only _PARSING.md used)
[parse_courses.py]
    ↓
final.json
```

## How to Verify Nothing Was Lost

1. **From the TOC version**: Count lessons listed
   ```bash
   grep "^### " output/121\ PHILS\ TEXT.md | grep -v "\..*\.\.\." | wc -l
   ```

2. **From the parsing version**: Count extracted lessons
   ```bash
   jq '.lessons | length' data/d1_final.json
   ```

3. **Compare**: Should match (minus TOC entries that have dot leaders)

## Cleanup Script Usage

To regenerate cleaned files without modifying originals:

```bash
python cleanup_markdown.py
# Creates: *_PARSING.md files
# Leaves: Original .md files untouched
```

## Table of Contents Preserved At

The Table of Contents can be viewed in the original markdown files.

For 121 PHILS TEXT.md:
- Lines contain lesson list with page numbers
- Example: `### Encounter 1: Who Is Jesus Christ? ........................................ 3`
- These are marked with dot leaders (`\.\.\.`) for easy filtering

## Recovery

### If *_PARSING files get corrupted:
```bash
python cleanup_markdown.py
# Regenerates _PARSING.md files from originals
```

### If Original .md files with TOC are lost:

The originals with Table of Contents can be regenerated from PDF files using the `pdf_to_markdown_course` skill:

```bash
# Run the skill on the original PDF files to regenerate markdown with TOC intact
/pdf-to-markdown-course <pdf_file>
```

This will recreate the original .md files with the Table of Contents section preserved.

## Current State (2026-08-08)

- **Original .md files**: Currently TOC-removed (regenerate if needed via pdf_to_markdown_course skill)
- **_PARSING.md files**: Ready to use with parser  
- **Workflow established**: Future changes follow the markdown pipeline documented above
