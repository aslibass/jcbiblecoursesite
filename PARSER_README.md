# Course Markdown Parser

This directory contains tools to parse Bible course markdown files into structured JSON.

## Status

We've created parsers to convert the markdown files (121 PHILS TEXT.md, CL TEXT PHILS.md, GALATIANS PHILS TEXT.md) into structured course data, but they need refinement.

## Files

- `parse_courses_v2.py` - The improved parser that correctly identifies lessons but needs content parsing work
- `courses_final.json` - Output from v2 parser (lesson titles correct, but no content extracted yet)
- `data/d1_final.json`, `data/cl_final.json`, `data/gal_final.json` - Individual course outputs

## Problem Identified

The original course JSON in Claude Design has **all content flattened into a single blocks array** with no proper section structure. This makes the lessons flow unnaturally.

### Original (Broken) Structure:
```json
{
  "blocks": [
    {"t":"h1","x":"LESSON OUTLINE LESSON OBJECTIVES"},  // Merged!
    {"t":"h2","x":"A. A Perfect Human 1. Understand..."},  // Mixed content
    {"t":"li","x":"2. Describe who Jesus is..."},  // Out of order
    // ... hundreds of mixed items
  ]
}
```

### Desired Structure:
```json
{
  "objectives": ["Understand...", "Describe..."],
  "assignments": ["Study lesson...", "Memorize..."],
  "sections": [
    {
      "title": "A. A Perfect Human",
      "blocks": [
        {"t":"p", "x":"Paragraph..."},
        {"t":"q", "n":"1", "x":"Question text"}
      ]
    }
  ]
}
```

## Next Steps to Fix

1. **Debug section extraction**: The `extract_sections()` function needs to properly find:
   - `LESSON OBJECTIVES` section
   - `ASSIGNMENTS` section
   - `LESSON DEVELOPMENT` section

2. **Preserve content hierarchy**: Don't flatten everything into one blocks array

3. **Test on each markdown file**: They may have slightly different formatting

4. **Validate output**: Ensure every lesson has:
   - Objectives array (not empty)
   - Assignments array (not empty)
   - Content blocks with questions

## How to Improve the Parser

1. Run the parser and check output
2. Pick a lesson that's empty and manually inspect that section of the markdown
3. Add debug logging to see where sections start/end
4. Fix the regex patterns that detect section boundaries
5. Test incremental improvements

## Quick Test

```bash
python parse_courses_v2.py
# Check output: courses_final.json and data/*_final.json
```

Then inspect a lesson's markdown section to debug why sections aren't being extracted.
