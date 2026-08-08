#!/usr/bin/env python3
"""Add exams to course with questions from lessons"""
import json

def add_exams(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for course in data:
        lessons = course.get('lessons', [])

        # Extract questions from lessons
        exam_questions = []
        for lesson_idx, lesson in enumerate(lessons):
            blocks = lesson.get('blocks', [])
            q_blocks = [b for b in blocks if b.get('t') == 'q']

            # Take 2-3 questions per lesson for exam
            for qb in q_blocks[:2]:
                exam_questions.append({
                    "n": str(len(exam_questions) + 1),
                    "type": "short",
                    "text": qb.get('x', 'Question'),
                    "marks": 3
                })

        # Create final exam
        course['exams'] = [{
            "title": "Final Exam - " + course.get('short', 'Course'),
            "scope": "full",
            "unit": None,
            "questions": exam_questions[:20]  # 20 questions max
        }]

        print(f"✓ Added exam to {course['title']} with {len(course['exams'][0]['questions'])} questions")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_exams('public/data/courses.json')
print("\n✓ Exams added and saved")
