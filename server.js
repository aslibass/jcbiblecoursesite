#!/usr/bin/env node
/**
 * Simple Express server to host Claude Design course site
 * Serves the .dc.html file and course JSON data
 * Provides exam grading via Claude API
 */

const express = require('express');
const path = require('path');
const crypto = require('crypto');
const app = express();

const PORT = process.env.PORT || 3000;
const SITE_PASSWORD = process.env.SITE_PASSWORD || 'biblestudy';

// Parse JSON request bodies
app.use(express.json());

// Authentication middleware
function isAuthenticated(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '') || req.query.token;
  if (token && token === crypto.createHash('sha256').update(SITE_PASSWORD).digest('hex')) {
    return next();
  }

  const sessionToken = req.body?.token || req.query?.token;
  if (sessionToken && sessionToken === crypto.createHash('sha256').update(SITE_PASSWORD).digest('hex')) {
    return next();
  }

  res.status(401).sendFile(path.join(__dirname, 'public', 'login.html'));
}

// Redirect unauth to login
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Claude API client (if available)
let claudeClient = null;
try {
  const Anthropic = require('@anthropic-ai/sdk');
  claudeClient = new Anthropic({
    apiKey: process.env.CLAUDE_API_KEY
  });
} catch (e) {
  console.warn('⚠️  Claude SDK not installed. Exam auto-grading will be unavailable.');
}

// Serve static files with proper UTF-8 charset
app.use(express.static(path.join(__dirname, 'public'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html')) {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
    } else if (filePath.endsWith('.json')) {
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
    } else if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
    }
  }
}));

// Serve JSON data
app.use('/data', express.static(path.join(__dirname, 'data')));

// Login endpoint
app.post('/api/login', (req, res) => {
  const { password } = req.body;
  if (password === SITE_PASSWORD) {
    const token = crypto.createHash('sha256').update(SITE_PASSWORD).digest('hex');
    res.json({ success: true, token });
  } else {
    res.status(401).json({ success: false, error: 'Invalid password' });
  }
});

// Logout endpoint
app.get('/logout', (req, res) => {
  res.redirect('/login');
});

// Landing page (public)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'landing.html'));
});

// Course platform (protected)
app.get('/courses', isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Exam grading endpoint (Claude AI)
app.post('/api/grade-exam', async (req, res) => {
  if (!claudeClient) {
    return res.status(503).json({ error: 'Grading service unavailable' });
  }

  try {
    const { courseContent, exam, answers } = req.body;

    const payload = exam.questions.map(q => ({
      n: q.n, type: q.type, marks: q.marks, question: q.text,
      options: q.opts, answer: answers[q.n] || ''
    }));

    const response = await claudeClient.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4000,
      system: 'You grade a Bible-course exam using only the supplied course material as the standard. Return ONLY a JSON array, no prose, no code fence. Each element: {"n": "<question number>", "score": <number 0..marks>, "feedback": "<one or two sentences>"}. Be fair but exact.',
      messages: [{
        role: 'user',
        content: `COURSE MATERIAL:\n${courseContent}\n\nEXAM:\n${JSON.stringify(payload)}`
      }]
    });

    const content = response.content[0].text;
    const match = content.match(/\[[^\[\]]*\]/);
    const parsed = JSON.parse(match ? match[0] : content);

    res.json({ success: true, results: parsed });
  } catch (error) {
    console.error('Grading error:', error);
    res.status(500).json({ error: 'Grading failed' });
  }
});

// Health check for Railway
app.get('/health', (req, res) => {
  res.json({ status: 'ok', claudeGrading: !!claudeClient });
});

app.listen(PORT, () => {
  console.log(`🚀 Course site running on http://localhost:${PORT}`);
  console.log(`📚 Serving courses from /data/courses_final.json`);
});
