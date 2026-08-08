# BEE Study Center – Deployment Guide

## 🚀 Live Platform

**Landing Page:** https://jcbiblecoursesite-production.up.railway.app  
**Course Platform:** https://jcbiblecoursesite-production.up.railway.app/courses  
**GitHub:** https://github.com/aslibass/jcbiblecoursesite

---

## ✅ What's Deployed

### Content
- **3 Courses** with 34 total lessons
  - Discipleship Training (15 lessons)
  - Christian Life Studies (12 lessons)
  - Galatians Study (7 lessons)
- **224 Study Questions** extracted from lessons
- **Final Exam** with 20 questions (per course)
- All lessons properly titled and structured

### Features
- Student & teacher dashboard views
- Progress tracking via localStorage
- Interactive lesson content with study questions
- Final exams with AI-powered grading
- Responsive design for mobile/tablet/desktop

### Technical
- Node.js + Express server
- Claude Design component system (React-based)
- Proper UTF-8 encoding (fixed encoding issues)
- Course data loaded from `/data/courses.json`
- Auto-charset headers on all responses

---

## 🔧 Configuration

### Claude API for Exam Grading

The platform includes AI-powered exam grading. To enable it:

1. **Get API Key**
   - Go to https://console.anthropic.com/account/keys
   - Create a new API key
   - Copy the key

2. **Set on Railway**
   - Go to https://railway.com/project/bcf88150-91a4-47c9-8aec-0db1b1fd5189
   - Click **jcbiblecoursesite** service
   - Go to **Variables** tab
   - Add variable:
     ```
     CLAUDE_API_KEY = sk-ant-...your-key...
     ```
   - Railway auto-redeploys after variable save

3. **Test Grading**
   - Visit platform
   - Log in as student
   - Take Final Exam
   - Click "Submit for grading"
   - Claude AI will grade and provide feedback

### Without API Key
The platform works fine without the API key:
- All courses and lessons accessible
- Study questions available
- Exams can be taken
- Auto-grading won't work (manual grading only)

---

## 📁 File Structure

```
.
├── server.js                    # Express server with API endpoints
├── package.json                 # Node dependencies
├── Dockerfile                   # Railway deployment config
├── public/
│   ├── landing.html            # Landing page (route: /)
│   ├── index.html              # Course platform (route: /courses)
│   ├── support.js              # Claude Design runtime
│   └── data/
│       └── courses.json        # Course content (all 3 courses)
├── data/
│   ├── d1_final.json           # Discipleship Training
│   ├── cl_final.json           # Christian Life
│   └── gal_final.json          # Galatians
└── input/
    ├── 121 PHILS TEXT.pdf
    ├── CL TEXT PHILS.pdf
    └── GALATIANS PHILS TEXT.pdf
```

---

## 🔄 Deployment Process

### Automatic Deployment
1. Push to `master` branch on GitHub
2. Railway detects the push
3. Automatic build + deploy (takes ~2-3 minutes)
4. Live at https://jcbiblecoursesite-production.up.railway.app

### Manual Deployment
```bash
git push origin master
```

---

## 🐛 Troubleshooting

### Platform Won't Load
- Check Railway logs: https://railway.com/project/bcf88150-91a4-47c9-8aec-0db1b1fd5189
- Verify React CDN links load (check browser console)
- Clear browser cache

### Exam Grading Not Working
- Check `CLAUDE_API_KEY` variable is set on Railway
- Verify API key is valid at console.anthropic.com
- Check Railway logs for grading errors

### Courses Not Loading
- Verify `/data/courses.json` exists on server
- Check server logs for fetch errors
- Ensure JSON is valid

---

## 📊 Endpoints

| Route | Purpose |
|-------|---------|
| `GET /` | Landing page |
| `GET /courses` | Course platform |
| `GET /data/courses.json` | Course JSON (students, lessons, questions) |
| `POST /api/grade-exam` | Grade exam with Claude AI |
| `GET /health` | Health check (shows if grading available) |

---

## 🔐 Security Notes

- API key stored as Railway environment variable (secure)
- No sensitive data in public HTML
- CORS not enabled (same-origin only)
- localStorage used for client-side progress (not synced)

---

## 📝 Updates & Maintenance

### To Update Course Content
1. Edit `/data/d1_final.json` (or other course files)
2. Run: `python add_exams.py` (regenerate exams)
3. Push to GitHub
4. Railway auto-deploys

### To Update Landing Page
1. Edit `/public/landing.html`
2. Push to GitHub
3. Railway auto-deploys

### To Fix Lessons
1. Check `/data/d1_final.json` structure
2. Verify lessons have proper titles, blocks, and questions
3. Run fixes if needed
4. Push updates

---

## ✨ Next Steps

1. **Set Claude API Key** (for auto-grading)
2. **Test the platform** at /courses
3. **Monitor analytics** via Railway dashboard
4. **Collect feedback** from students/teachers
5. **Update content** as needed

---

**Created:** 2026-08-08  
**Platform:** Railway + Node.js + Claude Design  
**Status:** ✅ Live and ready
