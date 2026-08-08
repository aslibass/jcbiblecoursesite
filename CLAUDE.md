# BEE Study Center – Claude Code Workflow

## Project Overview

Complete PDF-to-platform workflow for creating interactive Bible course study platforms. Converts PDFs → JSON → interactive web platform with authentication, progress tracking, and AI-powered exam grading.

## Quick Start

### To add a new course from PDF:

```bash
/pdf-to-markdown-course          # Extract & structure PDF
# Review output in data/*.json
git add -A && git commit -m "Add new course module"
git push origin master           # Railway auto-deploys
```

---

## Complete Workflow (End-to-End)

### Phase 1: PDF Extraction & Cleanup
```
User provides: PDF file(s)
     ↓
/pdf-to-markdown-course skill
     ↓
Outputs: data/*_final.json (with known issues - see below)
     ↓
Auto-fix scripts run:
  • fix_lesson_titles.py (correct broken titles from PDF TOC)
  • add_exams.py (create exams from questions)
     ↓
Outputs: data/courses_final.json (combined, fixed)
     ↓
Copies to: public/data/courses.json (served to frontend)
```

### Phase 2: Platform Display
```
public/index.html (Claude Design component)
     ↓
Loads: public/data/courses.json via fetch
     ↓
Renders: Interactive lessons, questions, exams
     ↓
Features:
  • Student view: lessons, questions, progress tracking
  • Teacher view: roster, exams, student work review
  • AI grading: Claude API grades exams
```

### Phase 3: Deployment
```
Changes pushed to GitHub
     ↓
Railway webhook triggered
     ↓
Dockerfile builds: Node.js + dependencies
     ↓
Deploy: https://jcbiblecoursesite-production.up.railway.app
     ↓
Live: Login required → courses accessible
```

---

## Known Issues with pdf-to-markdown-course Skill

The skill is ~85% accurate but has systematic issues that MUST be fixed:

### Issue 1: Corrupted Lesson Titles
```
PDF Input:     "Lesson 1: Who Is Jesus Christ?"
Skill Output:  "<!-- CONTENT START - Table of Contents removed above -->"
```
**Fix:** Manually extract titles from PDF table of contents, update `TITLES` dict in fix_lesson_titles.py

### Issue 2: Fragmented Content Blocks
```
PDF Input:     "When meeting people for the first time, we often learn their names..."
Skill Output:  Block 1: "When meeting people for the first time, we often learn their names and a"
               Block 2: "brief introduction to their backgrounds. After more time is spent with"
               Block 3: "these new people, a deeper relationship grows..."
```
**Fix:** add_exams.py rejoins consecutive paragraph blocks

### Issue 3: Page Numbers & Artifacts Mixed In
```
PDF Input:     (footer text "4 ● One-to-One Discipleship Training")
Skill Output:  Treated as actual lesson content
```
**Fix:** Filtered out by fix_lesson_titles.py

### Issue 4: UTF-8 Character Encoding Broken
```
PDF Input:     "Galatians – read the lessons"
Skill Output:  "Galatians â€" read the lessons"
```
**Fix:** Character encoding cleanup script

---

## Adding a New Course (Step-by-Step)

### Step 1: Extract
```bash
# Place PDF in input/ folder
/pdf-to-markdown-course
# Outputs: data/new_course_final.json
```

### Step 2: Review Output
```bash
# Check data/new_course_final.json
# ✓ Does lesson count look right?
# ✓ Are questions extracted?
# ✗ Are lesson titles garbage? → EXPECTED, fix next
# ✗ Is content fragmented? → EXPECTED, fix next
```

### Step 3: Fix Lesson Titles
Edit `fix_lesson_titles.py`:

```python
TITLES = {
    "d1": ["Who Is Jesus Christ?", "What Did Jesus Do?", ...],
    "cl": ["Lesson 1: Title", ...],
    "new": ["Lesson 1", "Lesson 2", ...],  # ADD NEW COURSE HERE
}
```

Look up titles in PDF table of contents (first 5 pages)

### Step 4: Run Fix Scripts
```bash
python fix_lesson_titles.py    # Fix titles & structure
python add_exams.py            # Create exams from questions
```

### Step 5: Test Locally
```bash
npm start
# Open: http://localhost:3000
# Password: biblestudy
# Verify:
#   ✓ New course appears in dashboard
#   ✓ Click course → see all lessons with correct titles
#   ✓ Click lesson → see content (no HTML comments)
#   ✓ See study questions
#   ✓ Final Exam available
#   ✓ Click exam → take test → submit for grading
```

### Step 6: Deploy
```bash
git add -A
git commit -m "Add course: Course Name

- X lessons with Y questions
- Z exam questions"
git push origin master
# Railway auto-deploys (2-3 min)
```

---

## Key Scripts & Their Purpose

| Script | Purpose | Run When |
|--------|---------|----------|
| `/pdf-to-markdown-course` | Extract PDF to JSON | Adding new course from PDF |
| `fix_lesson_titles.py` | Fix broken lesson titles, remove artifacts | After extraction, update TITLES dict first |
| `add_exams.py` | Create final exams | After fixing titles |
| `server.js` | Express server, auth, API | Always running |
| `public/index.html` | Claude Design platform | Never edit directly |
| `public/login.html` | Password login | Never edit directly |
| `public/landing.html` | Public landing page | Can customize |

---

## Configuration

### Local Development
```bash
PORT=3000
SITE_PASSWORD=biblestudy
CLAUDE_API_KEY=sk-ant-xxx  # For exam grading
npm start
```

### Railway Platform
Go to project → service → Variables:
```
SITE_PASSWORD = your-password
CLAUDE_API_KEY = sk-ant-your-api-key
```

---

## Orchestration Flow

```
1. USER: Provides PDF file
   ↓
2. /pdf-to-markdown-course (SKILL)
   └→ Outputs: data/*_final.json (90% done, needs manual fixes)
   ↓
3. DEVELOPER: Review & update fix_lesson_titles.py TITLES dict
   ↓
4. python fix_lesson_titles.py (SCRIPT)
   ├→ Replaces garbage titles with correct names
   ├→ Removes page numbers/artifacts
   └→ Rejoins fragmented blocks
   ↓
5. python add_exams.py (SCRIPT)
   └→ Creates exams from lesson questions
   ↓
6. npm start (TEST LOCALLY)
   └→ Verify courses load correctly
   ↓
7. git push origin master (DEPLOY)
   └→ Railway auto-deploys
   ↓
8. LIVE: https://jcbiblecoursesite-production.up.railway.app
```

---

## Files to Know

```
data/
├── d1_final.json              ← After /pdf-to-markdown-course (review & verify)
├── cl_final.json
├── gal_final.json
└── courses_final.json         ← Auto-generated, don't edit

public/
├── index.html                 ← Claude Design platform (don't edit!)
├── login.html                 ← Password page (don't edit!)
├── landing.html               ← Public landing (can customize)
├── support.js                 ← Claude Design runtime (don't edit!)
└── data/
    └── courses.json           ← Copy of data/courses_final.json

fix_lesson_titles.py           ← UPDATE TITLES dict for new courses
add_exams.py                   ← Run after fixing titles
server.js                      ← Express app (can customize)
CLAUDE.md                      ← This file (orchestration guide)
DEPLOYMENT.md                  ← Detailed deployment instructions
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Lesson titles show `<!-- CONTENT START -->` | TITLES dict not updated | Update fix_lesson_titles.py, rerun script |
| Paragraphs fragmented across blocks | Skill default behavior | Run add_exams.py (rejoins blocks) |
| Characters show `â€"` instead of `–` | Encoding issue | Character encoding fix script |
| No questions appearing | Skill didn't extract | Check JSON has `"t": "q"` blocks, rerun add_exams.py |
| Exams won't grade | Missing API key | Set CLAUDE_API_KEY on Railway |
| Can't log in | Wrong password | Default: `biblestudy`, change via SITE_PASSWORD |

---

## MCP Servers

This project uses:
- **claude-design**: Access design projects and export components
- **railway**: Deploy to production

---

## Next Steps for Automation

Future improvements to skills:
- [ ] Enhance pdf-to-markdown-course to auto-detect lesson titles from TOC
- [ ] Auto-fix character encoding in skill output
- [ ] Detect and remove page numbers/artifacts automatically
- [ ] Create master orchestration skill that runs all fixes automatically
- [ ] Add validation step to verify course quality before deployment
