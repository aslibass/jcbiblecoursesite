#!/usr/bin/env python3
"""
Improved course parser that properly handles the complex markdown structure.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

class CourseParserV2:
    def __init__(self, markdown_file: str, course_id: str, course_title: str, course_short: str, edition: str):
        self.file_path = Path(markdown_file)
        self.course_id = course_id
        self.course_title = course_title
        self.course_short = course_short
        self.edition = edition
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
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

    def is_table_of_contents_line(self, line: str) -> bool:
        """Check if line is from table of contents (has dot leaders)."""
        # TOC lines have patterns like "### Lesson 1 .............. 5"
        return bool(re.search(r'\.{4,}', line))

    def is_actual_lesson_header(self, line: str) -> bool:
        """Check if this is an actual lesson header, not TOC."""
        # Should match ### Encounter 1: ... or ### Lesson 1: ...
        # But NOT if it has dot leaders
        if self.is_table_of_contents_line(line):
            return False
        if not re.match(r'^###\s+(?:Encounter|Lesson|Quiet Time)', line):
            return False
        return True

    def extract_sections(self, start_line: int, end_line: int) -> Tuple[List[str], List[str], List[str]]:
        """Extract objectives, assignments, and content blocks from a lesson section."""
        objectives = []
        assignments = []
        blocks = []

        current_section = None
        last_assignment_idx = -1

        # First pass: find section boundaries
        for i in range(start_line, end_line):
            line_strip = self.lines[i].strip()
            if re.match(r'^ASSIGNMENTS', line_strip):
                last_assignment_idx = i

        # Second pass: extract content
        for i in range(start_line, end_line):
            line = self.lines[i]
            line_strip = line.strip()

            # Detect section markers
            if re.match(r'^LESSON OUTLINE', line_strip):
                current_section = 'outline'
                continue
            elif re.match(r'^LESSON OBJECTIVES', line_strip):
                current_section = 'objectives'
                continue
            elif re.match(r'^ASSIGNMENTS', line_strip):
                current_section = 'assignments'
                continue
            elif re.match(r'^LESSON DEVELOPMENT', line_strip):
                current_section = 'content'
                continue

            if not line_strip:
                continue

            # Switch from 'assignments' to 'content' after assignments block
            if current_section == 'assignments' and i > last_assignment_idx and last_assignment_idx >= start_line:
                current_section = 'content'

            # Process based on current section
            if current_section == 'objectives':
                text = line_strip.strip('*').strip()
                if text and not text.startswith('#') and not text.startswith('####'):
                    if re.match(r'^\d+\.\s+', text):
                        objectives.append(re.sub(r'^\d+\.\s+', '', text))

            elif current_section == 'assignments':
                text = line_strip.strip('*').strip()
                if text and not text.startswith('#') and not text.startswith('####'):
                    if re.match(r'^\d+\.\s+', text):
                        assignments.append(re.sub(r'^\d+\.\s+', '', text))

            elif current_section == 'content':
                # In content section (either LESSON DEVELOPMENT or after ASSIGNMENTS)
                block = self.parse_content_block(line)
                if block:
                    blocks.append(block)

        return objectives, assignments, blocks

    def parse_content_block(self, line: str) -> Dict[str, Any] | None:
        """Parse a single content line into a block structure."""
        line_stripped = line.strip()

        if not line_stripped:
            return None

        # Skip certain markers
        if line_stripped in ['Objective 1:', 'Objective 2:', 'Objective 3:', 'Objective 4:']:
            return None
        if re.match(r'^Objective\s+\d+:', line_stripped):
            return None

        # Section header (#### A. Title or #### A. Title N. Objective)
        if re.match(r'^####\s+[A-Z]\.\s+', line_stripped):
            # Extract just the section title, not inline objectives
            text = re.sub(r'(\d+\.\s+.+)$', '', line_stripped.lstrip('#').strip()).strip()
            if text:
                return {
                    "t": "h2",
                    "x": text
                }
            return None

        # Main heading (## Title)
        elif re.match(r'^##\s+', line_stripped):
            return {
                "t": "h1",
                "x": line_stripped.lstrip('#').strip()
            }

        # Question format: "> **Question N: ..." (most common format)
        elif re.match(r'^>\s*\*\*Question\s+(\d+):', line_stripped):
            # Extract question number and text (may span multiple lines in markdown)
            match = re.match(r'^>\s*\*\*Question\s+(\d+):\s*(.+?)\*\*?\s*$', line_stripped)
            if match:
                q_num = match.group(1)
                q_text = match.group(2).strip()
                return {
                    "t": "q",
                    "n": q_num,
                    "x": q_text
                }
            # Fallback: match with just colon
            match = re.match(r'^>\s*\*\*Question\s+(\d+):\s*(.*)$', line_stripped)
            if match:
                q_num = match.group(1)
                q_text = match.group(2).replace('**', '').strip()
                if q_text:
                    return {
                        "t": "q",
                        "n": q_num,
                        "x": q_text
                    }

        # List items: "a) text", "b) text" (sub-answers to questions)
        elif re.match(r'^[a-z]\)\s+', line_stripped):
            return {
                "t": "li",
                "x": line_stripped
            }

        # Scripture references in italics/bold: "***Matthew 2:1***, 23"
        elif re.match(r'^\*{2,}\w+', line_stripped):
            text = line_stripped
            text = re.sub(r'\*{2,}(.+?)\*{2,}', r'\1', text)
            if text.strip():
                return {
                    "t": "p",
                    "x": text.strip()
                }
            return None

        # Regular paragraph (not a header or special format)
        elif line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('**Objective') and not line_stripped.startswith('**Question'):
            # Clean formatting
            text = line_stripped
            text = re.sub(r'\*{3}(.+?)\*{3}', r'\1', text)    # Remove ***bold-italic***
            text = re.sub(r'\*{2}(.+?)\*{2}', r'\1', text)    # Remove **bold**
            text = re.sub(r'\*(.+?)\*', r'\1', text)          # Remove *italic*
            text = re.sub(r'^>\s+', '', text)                 # Remove blockquote marker
            text = text.strip()

            if text and len(text) > 2:  # Ignore single characters (page numbers, bullets, etc.)
                return {
                    "t": "p",
                    "x": text
                }

        return None

    def extract_lessons(self):
        """Find and extract all lessons based on LESSON OUTLINE markers."""
        lesson_outline_indices = []

        # Find all LESSON OUTLINE markers
        for i, line in enumerate(self.lines):
            if re.match(r'^LESSON OUTLINE', line.strip()):
                lesson_outline_indices.append(i)

        if not lesson_outline_indices:
            print(f"  Warning: No lessons found in {self.file_path.name}")
            return

        # Process each lesson
        for lesson_idx, outline_idx in enumerate(lesson_outline_indices):
            # Find the lesson title (go back from LESSON OUTLINE to find it)
            # Collect previous non-empty, non-header lines
            title_parts = []
            for j in range(outline_idx - 1, max(outline_idx - 10, -1), -1):
                line = self.lines[j].strip()
                if line and not line.startswith('#'):
                    # Skip section markers and certain keywords
                    if not re.match(r'^LESSON|^ASSIGNMENTS|^OBJECTIVES', line):
                        title_parts.insert(0, line)  # Insert at beginning to maintain order
                    if len(title_parts) >= 3:  # Collect up to 3 lines
                        break
                elif not line and title_parts:  # Empty line after collecting title parts
                    break

            lesson_title = ' '.join(title_parts) if title_parts else f"Lesson {lesson_idx + 1}"
            # Clean up the title
            lesson_title = re.sub(r'\d+\s*●', '', lesson_title).strip()  # Remove page numbers like "5 ●"

            # Find end of this lesson (start of next LESSON OUTLINE or end of file)
            end_idx = lesson_outline_indices[lesson_idx + 1] if lesson_idx + 1 < len(lesson_outline_indices) else len(self.lines)

            # Extract objectives, assignments, and content
            objectives, assignments, blocks = self.extract_sections(outline_idx, end_idx)

            # Create lesson object
            lesson = {
                "num": lesson_title,
                "title": lesson_title,
                "objectives": objectives,
                "assignments": assignments,
                "blocks": blocks,
                "qCount": sum(1 for b in blocks if b.get("t") == "q")
            }

            self.lessons.append(lesson)

        # Extract units based on lesson numbering
        self.extract_units()

    def extract_units(self):
        """Group lessons into units based on their content."""
        # For now, put all lessons in a single unit
        # TODO: Implement better unit detection based on course structure
        if self.lessons:
            self.units = [{
                "n": "Unit I",
                "t": "All Lessons",
                "l": list(range(len(self.lessons)))
            }]

def main():
    """Parse all course markdown files."""
    courses_config = [
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/121 PHILS TEXT_PARSING.md",
            "id": "d1",
            "title": "One-to-One Discipleship Training",
            "short": "Discipleship",
            "edition": "3rd Edition"
        },
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/CL TEXT PHILS_PARSING.md",
            "id": "cl",
            "title": "Christian Life",
            "short": "Christian Life",
            "edition": "1st Edition"
        },
        {
            "file": "C:/Users/viren/source/jcbiblecourse/output/GALATIANS PHILS TEXT_PARSING.md",
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
            parser = CourseParserV2(
                config["file"],
                config["id"],
                config["title"],
                config["short"],
                config["edition"]
            )
            course_data = parser.parse()
            all_courses.append(course_data)
            print(f"  ✓ Extracted {len(course_data['lessons'])} lessons with {sum(l.get('qCount', 0) for l in course_data['lessons'])} total questions")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()

    # Write combined output
    output_file = Path("C:/Users/viren/source/jcbiblecourse/courses_final.json")
    output_file.write_text(json.dumps(all_courses, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n✓ Saved all courses to {output_file}")

    # Save individual course files
    for course in all_courses:
        course_file = Path(f"C:/Users/viren/source/jcbiblecourse/data/{course['id']}_final.json")
        course_file.parent.mkdir(exist_ok=True)
        course_file.write_text(json.dumps(course, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"✓ Saved {course_file}")

if __name__ == "__main__":
    main()
