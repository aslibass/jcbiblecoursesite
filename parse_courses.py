#!/usr/bin/env python3
"""
Parse Bible course markdown files into structured JSON.
Properly extracts lessons, objectives, assignments, and content sections.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

class CourseParser:
    def __init__(self, markdown_file: str, course_id: str, course_title: str, course_short: str, edition: str):
        self.file_path = Path(markdown_file)
        self.course_id = course_id
        self.course_title = course_title
        self.course_short = course_short
        self.edition = edition
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lessons: List[Dict[str, Any]] = []
        self.units: List[Dict[str, Any]] = []

    def parse(self) -> Dict[str, Any]:
        """Main parsing method."""
        self.extract_lessons()
        return {
            "id": self.course_id,
            "title": self.course_title,
            "short": self.course_short,
            "edition": self.edition,
            "units": self.units,
            "lessons": self.lessons,
            "exams": []
        }

    def extract_lessons(self):
        """Extract all lessons from the markdown content."""
        # Skip table of contents and intro material
        lines = self.content.split('\n')

        # Find where actual content starts (look for first lesson with content)
        start_idx = 0
        for i, line in enumerate(lines):
            if re.match(r'^# UNIT|^# Unit', line):
                start_idx = i
                break

        lines = lines[start_idx:]

        current_lesson = None
        current_section = None
        in_objectives = False
        in_assignments = False
        in_lesson_dev = False
        objectives = []
        assignments = []
        content_blocks = []

        for i, line in enumerate(lines):
            # Detect lesson start (### Lesson Name or ### Encounter N:)
            if re.match(r'^###\s+(?:Encounter|Lesson|Quiet Time)', line) and not re.match(r'^####', line):
                # Save previous lesson if exists
                if current_lesson:
                    self.save_lesson(current_lesson, objectives, assignments, content_blocks)

                # Start new lesson
                lesson_match = re.match(r'^###\s+(.+)$', line)
                if lesson_match:
                    title = lesson_match.group(1).strip()
                    # Extract lesson number if present
                    num_match = re.match(r'^((?:Encounter|Lesson|Quiet Time)\s+\d*\.?\s*[^:]*?)(?:\s*:(.*))?$', title)
                    if num_match:
                        lesson_num = num_match.group(1).strip()
                        lesson_title = num_match.group(2).strip() if num_match.group(2) else lesson_num
                    else:
                        lesson_num = title
                        lesson_title = title

                    current_lesson = {
                        "num": lesson_num,
                        "title": lesson_title
                    }
                    objectives = []
                    assignments = []
                    content_blocks = []
                    in_objectives = False
                    in_assignments = False
                    in_lesson_dev = False
                    current_section = None

            elif not current_lesson:
                continue

            # Detect section markers
            elif re.match(r'^LESSON OUTLINE', line):
                in_lesson_dev = False
                in_objectives = False
                in_assignments = False
                current_section = None
            elif re.match(r'^LESSON OBJECTIVES', line):
                in_objectives = True
                in_assignments = False
                in_lesson_dev = False
                current_section = None
            elif re.match(r'^ASSIGNMENTS', line):
                in_assignments = True
                in_objectives = False
                in_lesson_dev = False
                current_section = None
            elif re.match(r'^(?:LESSON DEVELOPMENT|WORD STUDY)', line):
                in_lesson_dev = True
                in_objectives = False
                in_assignments = False
                current_section = None

            # Process content based on current section
            elif in_objectives:
                if re.match(r'^#{1,4}\s', line) or re.match(r'^[A-Z]{2,}', line):
                    in_objectives = False
                    in_assignments = False
                    continue
                self.process_objective_line(line, objectives)

            elif in_assignments:
                if re.match(r'^#{1,4}\s', line) or re.match(r'^[A-Z]{2,}', line):
                    in_assignments = False
                    continue
                self.process_assignment_line(line, assignments)

            elif in_lesson_dev:
                if re.match(r'^###\s+(?:Encounter|Lesson|Quiet Time)', line):
                    in_lesson_dev = False
                    continue
                self.process_content_line(line, content_blocks)

        # Save last lesson
        if current_lesson:
            self.save_lesson(current_lesson, objectives, assignments, content_blocks)

        # Extract units from content
        self.extract_units()

    def save_lesson(self, lesson: Dict, objectives: List[str], assignments: List[str], blocks: List[Dict]):
        """Save a lesson with its structured content."""
        lesson["objectives"] = objectives
        lesson["assignments"] = assignments
        lesson["blocks"] = blocks
        lesson["qCount"] = sum(1 for b in blocks if b.get("t") == "q")
        self.lessons.append(lesson)

    def process_objective_line(self, line: str, objectives: List[str]):
        """Extract objectives from objective lines."""
        line = line.strip()
        if not line:
            return

        # Remove numbering if present
        line = re.sub(r'^[\d\.]+\s+', '', line)
        # Remove bold markers
        line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)

        if line and line not in objectives:
            objectives.append(line)

    def process_assignment_line(self, line: str, assignments: List[str]):
        """Extract assignments from assignment lines."""
        line = line.strip()
        if not line:
            return

        # Remove numbering if present
        line = re.sub(r'^[\d\.]+\s+', '', line)
        # Remove bold markers
        line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)

        if line and line not in assignments:
            assignments.append(line)

    def process_content_line(self, line: str, blocks: List[Dict]):
        """Convert markdown content lines to block structure."""
        line_stripped = line.strip()

        if not line_stripped:
            return

        # Main section header (#### A. Title or #### A. Title ...)
        if re.match(r'^####\s+[A-Z]\.\s+', line_stripped):
            blocks.append({
                "t": "h2",
                "x": line_stripped.lstrip('#').strip()
            })

        # Subsection (##### or deeper)
        elif re.match(r'^#{5,}\s+', line_stripped):
            blocks.append({
                "t": "h3",
                "x": line_stripped.lstrip('#').strip()
            })

        # Main heading (# Title or ## Title)
        elif re.match(r'^##\s+', line_stripped):
            blocks.append({
                "t": "h1",
                "x": line_stripped.lstrip('#').strip()
            })

        # Question marker: "> **Question N:" or "Question N:"
        elif re.match(r'^>\s*\*\*Question\s+(\d+)', line_stripped):
            match = re.match(r'^>\s*\*\*Question\s+(\d+):\s*(.+?)\*\*', line_stripped)
            if match:
                q_num = match.group(1)
                q_text = match.group(2)
                blocks.append({
                    "t": "q",
                    "n": q_num,
                    "x": q_text
                })
        elif re.match(r'^Question\s+(\d+):', line_stripped):
            match = re.match(r'^Question\s+(\d+):\s*(.+)$', line_stripped)
            if match:
                q_num = match.group(1)
                q_text = match.group(2)
                blocks.append({
                    "t": "q",
                    "n": q_num,
                    "x": q_text
                })

        # List item: "- " or "a) " or "1. "
        elif re.match(r'^[a-z\d\-]\)\s+', line_stripped):
            blocks.append({
                "t": "li",
                "x": line_stripped
            })
        elif re.match(r'^-\s+', line_stripped):
            blocks.append({
                "t": "li",
                "x": line_stripped.lstrip('- ').strip()
            })

        # Special markers
        elif re.match(r'^Note:', line_stripped, re.IGNORECASE):
            blocks.append({
                "t": "note",
                "x": line_stripped.replace('Note:', '').strip()
            })
        elif re.match(r'^Objective\s+\d+:', line_stripped):
            blocks.append({
                "t": "note",
                "x": line_stripped
            })

        # Regular paragraph
        elif line_stripped:
            # Clean up formatting
            text = line_stripped
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
            text = re.sub(r'\*(.+?)\*', r'\1', text)  # Remove italic
            text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # Remove bold italic
            text = re.sub(r'_(.+?)_', r'\1', text)  # Remove underline
            text = re.sub(r'\(.*Matthew.*|.*John.*|.*Luke.*\)', lambda m: m.group(0).strip('()'), text)  # Keep scripture refs

            blocks.append({
                "t": "p",
                "x": text.strip()
            })

    def extract_units(self):
        """Extract unit structure from lessons."""
        # Determine units based on lesson numbering patterns
        units_map = {}

        for idx, lesson in enumerate(self.lessons):
            num = lesson["num"]

            # Encounter lessons -> Unit I
            if "Encounter" in num:
                unit_id = "I"
                unit_name = "Encounter"
            # Quiet Time -> Unit II
            elif "Quiet Time" in num:
                unit_id = "II"
                unit_name = "Fellowship"
            # Lesson 1-10 -> Unit III
            elif "Lesson" in num:
                unit_id = "III"
                unit_name = "Growth"
            else:
                continue

            if unit_id not in units_map:
                units_map[unit_id] = {
                    "n": f"Unit {unit_id}",
                    "t": unit_name,
                    "l": []
                }

            units_map[unit_id]["l"].append(idx)

        self.units = list(units_map.values())

def main():
    """Parse all course markdown files and generate courses.json."""

    courses_config = [
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/121 PHILS TEXT.md",
            "id": "d1",
            "title": "One-to-One Discipleship Training",
            "short": "Discipleship",
            "edition": "3rd Edition"
        },
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/CL TEXT PHILS.md",
            "id": "cl",
            "title": "Christian Life",
            "short": "Christian Life",
            "edition": "1st Edition"
        },
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/GALATIANS PHILS TEXT.md",
            "id": "gal",
            "title": "Galatians",
            "short": "Galatians",
            "edition": "1st Edition"
        }
    ]

    all_courses = []

    for config in courses_config:
        try:
            print(f"Parsing {config['title']}...")
            parser = CourseParser(
                config["file"],
                config["id"],
                config["title"],
                config["short"],
                config["edition"]
            )
            course_data = parser.parse()
            all_courses.append(course_data)
            print(f"  ✓ Extracted {len(course_data['lessons'])} lessons")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Write output
    output_file = Path("C:/Users/viren/source/jcbiblecourse/courses_structured.json")
    output_file.write_text(json.dumps(all_courses, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n✓ Saved to {output_file}")

    # Also save individual course files
    for course in all_courses:
        course_file = Path(f"C:/Users/viren/source/jcbiblecourse/{course['id']}_course.json")
        course_file.write_text(json.dumps(course, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"✓ Saved {course_file}")

if __name__ == "__main__":
    main()
