#!/bin/bash
# Setup script for local development

echo "🚀 Setting up BEE Study Center for local testing..."

# Create public/data directory if it doesn't exist
mkdir -p public/data

# Copy course data
if [ -f "data/courses_final.json" ]; then
  cp data/courses_final.json public/data/courses.json
  echo "✓ Copied course data to public/data/"
else
  echo "⚠ data/courses_final.json not found. Run /pdf-to-markdown-course first."
  exit 1
fi

# Install Node dependencies
if ! command -v npm &> /dev/null; then
  echo "❌ Node.js/npm not installed. Install from https://nodejs.org/"
  exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start local server:"
echo "  npm start"
echo ""
echo "Then open: http://localhost:3000"
echo ""
