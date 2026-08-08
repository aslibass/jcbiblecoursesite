#!/usr/bin/env python3
"""Fix lesson titles to match PDF table of contents"""
import json

# Correct lesson titles from PDF TOC
TITLES = {
    "d1": [
        "Who Is Jesus Christ?",
        "What Did Jesus Do?",
        "What Is Jesus Doing Now?",
        "Believing in Jesus Christ",
        "Quiet Time",
        "Assurance of Salvation",
        "Attributes of God",
        "Word of God: The Bible",
        "Prayer",
        "Fellowship",
        "Witnessing",
        "The Spirit-Filled Life",
        "Temptation",
        "Obedience",
        "Ministry"
    ]
}

def fix_course(file_path, course_id):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    titles = TITLES.get(course_id, [])
    lessons = data.get('lessons', [])

    # Rebuild with proper lesson structure
    for i, lesson in enumerate(lessons):
        # Set proper title
        if i < len(titles):
            lesson['title'] = titles[i]
            lesson['num'] = str(i + 1)

        # Remove corrupted content
        blocks = lesson.get('blocks', [])
        clean_blocks = []

        for block in blocks:
            if block.get('t') in ['p', 'q', 'h1', 'h2', 'li', 'note', 'ex']:
                clean_blocks.append(block)

        lesson['blocks'] = clean_blocks

        # Ensure there are objectives and assignments
        if not lesson.get('objectives'):
            lesson['objectives'] = []
        if not lesson.get('assignments'):
            lesson['assignments'] = []

    # Add exam if missing
    if 'exams' not in data:
        data['exams'] = [{
            "title": "Final Exam",
            "scope": "full",
            "questions": []
        }]

    # Ensure each exam has questions from lesson content
    for exam in data.get('exams', []):
        if not exam.get('questions'):
            # Generate basic questions from lessons
            questions = []
            for i, lesson in enumerate(lessons):
                q_blocks = [b for b in lesson.get('blocks', []) if b.get('t') == 'q']
                for qb in q_blocks[:3]:  # Take first 3 questions per lesson
                    questions.append({
                        "n": str(len(questions) + 1),
                        "type": "short",
                        "text": qb.get('x', 'Question'),
                        "marks": 2
                    })
            exam['questions'] = questions[:30]  # Limit to 30 questions

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ Fixed {file_path} with {len(lessons)} lessons")

# Fix all courses
fix_course('data/d1_final.json', 'd1')

# Regenerate combined file
all_courses = []
for course_file in ['data/d1_final.json']:
    with open(course_file, 'r', encoding='utf-8') as f:
        all_courses.append(json.load(f))

with open('data/courses_final.json', 'w', encoding='utf-8') as f:
    json.dump(all_courses, f, ensure_ascii=False, indent=2)

# Copy to public folder
import shutil
shutil.copy('data/courses_final.json', 'public/data/courses.json')
print("✓ Updated courses_final.json and public/data/courses.json")
