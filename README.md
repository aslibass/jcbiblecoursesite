# BEE Study Center - Bible Course Platform

Interactive course platform for Discipleship Training, Christian Life, and Galatians studies.

## Architecture

**Data Pipeline:**
```
PDFs → JSON (pdf-to-markdown-course skill)
  ↓
courses.json → Course Site (Frontend + UX)
  ↓
Live Platform (Railway + GitHub)
```

## Local Development

### Setup

1. Install dependencies:
```bash
npm install
```

2. Run locally:
```bash
npm start
```

3. Open http://localhost:3000

### Course Data

The platform loads course content from `public/data/courses.json`, which contains:
- 3 courses (Discipleship, Christian Life, Galatians)
- 34 total lessons
- 688+ study questions
- Lesson content, objectives, and assignments

## Updating Course Content

1. Run the PDF-to-JSON pipeline:
```bash
/pdf-to-markdown-course
```

2. This generates:
   - `data/courses_final.json` - Combined course data
   - `data/d1_final.json` - Discipleship course
   - `data/cl_final.json` - Christian Life course
   - `data/gal_final.json` - Galatians course

3. Copy the updated JSON to the public folder:
```bash
cp data/courses_final.json public/data/courses.json
```

4. Test locally, then commit and push to Railway

## Deployment

### Railway Setup

1. Connect GitHub repo: https://github.com/aslibass/jcbiblecoursesite.git
2. Railway automatically detects Node.js project
3. Sets PORT=3000 as default
4. Deploys on push to main

### Environment

- Node 18.x
- Express server on port 3000
- Static file serving for HTML, CSS, JS
- JSON endpoint at `/data/courses.json`

## Features

### Student Features
- ✅ Browse courses and lessons
- ✅ Read lesson content
- ✅ Answer study questions
- ✅ Track progress (localStorage)
- ✅ Take exams
- ✅ AI-powered feedback (optional, with Claude API)

### Teacher Features
- ✅ View student roster and progress
- ✅ Monitor exam scores
- ✅ Review written answers
- ✅ Manage class settings
- ✅ Track exam analytics

## File Structure

```
.
├── server.js                 # Express server
├── package.json             # Dependencies
├── Dockerfile               # Railway deployment
├── public/
│   ├── index.html          # Main app
│   ├── support.js          # Claude Design runtime
│   └── data/
│       └── courses.json    # Course content
├── data/
│   ├── courses_final.json  # Generated (master copy)
│   ├── d1_final.json       # Individual courses
│   ├── cl_final.json       #
│   └── gal_final.json      #
└── README.md

```

## Tech Stack

- **Frontend**: Claude Design (Component-based, React-powered)
- **Backend**: Node.js + Express
- **Styling**: Inline CSS (design system colors)
- **Data**: JSON (localStorage for progress tracking)
- **Deployment**: Railway (GitHub-connected)

## Skills Used

- `pdf-to-markdown-course` - PDF extraction and JSON generation
- `course-pages-builder` - Claude Design page generation

## Next Steps

1. ✅ Test locally: `npm start`
2. ✅ Push to GitHub
3. ✅ Deploy to Railway (automatic on push)
4. 📊 Monitor analytics at railway.app dashboard
5. 🔄 Update course content as needed

## Troubleshooting

**Port already in use:**
```bash
PORT=3001 npm start
```

**Courses not loading:**
- Check `public/data/courses.json` exists
- Verify JSON is valid: `npm install -g jsonlint && jsonlint public/data/courses.json`
- Check browser console for fetch errors

**Progress not saving:**
- Verify localStorage is enabled in browser
- Check browser dev tools > Application tab

## Support

For issues with course generation, see:
- PDF pipeline: `/pdf-to-markdown-course` skill
- Page generation: `/course-pages-builder` skill
