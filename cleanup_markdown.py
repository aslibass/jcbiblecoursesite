#!/usr/bin/env python3
"""
Clean up markdown files exported from PDFs.
Fixes formatting issues to ensure consistent structure for parsing.
"""

import re
from pathlib import Path

class MarkdownCleaner:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')

    def clean(self) -> str:
        """Apply all cleanup transformations."""
        self.remove_table_of_contents()
        self.separate_lesson_outline_objectives()
        self.fix_assignments_marker()
        self.fix_question_formatting()
        self.remove_page_artifacts()
        self.fix_section_consistency()

        return '\n'.join(self.lines)

    def remove_table_of_contents(self):
        """Remove everything before the first actual lesson."""
        # Find first LESSON OUTLINE marker - this is where real content begins
        first_content_idx = None

        for i, line in enumerate(self.lines):
            line_strip = line.strip()
            if re.match(r'^LESSON OUTLINE', line_strip):
                first_content_idx = i
                break

        if first_content_idx is not None:
            # Add marker for content start
            self.lines = ['<!-- CONTENT START - Table of Contents removed above -->', ''] + self.lines[first_content_idx:]
        # If not found, keep everything (fallback)

    def separate_lesson_outline_objectives(self):
        """Separate "LESSON OUTLINE LESSON OBJECTIVES" into two lines."""
        new_lines = []
        for line in self.lines:
            if re.match(r'^LESSON OUTLINE\s+LESSON OBJECTIVES', line.strip()):
                # Split into two separate lines
                new_lines.append("LESSON OUTLINE")
                new_lines.append("")
                new_lines.append("LESSON OBJECTIVES")
            else:
                new_lines.append(line)
        self.lines = new_lines

    def fix_assignments_marker(self):
        """Ensure ASSIGNMENTS has proper formatting."""
        new_lines = []
        for line in self.lines:
            # Change "# ASSIGNMENTS" to just "ASSIGNMENTS"
            if re.match(r'^#+\s*ASSIGNMENTS', line.strip()):
                new_lines.append("ASSIGNMENTS")
            else:
                new_lines.append(line)
        self.lines = new_lines

    def fix_question_formatting(self):
        """Normalize question formatting."""
        new_lines = []
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            line_strip = line.strip()

            # Match "> **Question N: text**"
            if re.match(r'^>\s*\*\*Question\s+\d+:', line_strip):
                # Ensure it's properly formatted
                match = re.match(r'^>\s*(\*\*Question\s+\d+:.*)', line_strip)
                if match:
                    # Keep the blockquote format but clean it up
                    new_lines.append('> ' + match.group(1))
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1

        self.lines = new_lines

    def remove_page_artifacts(self):
        """Remove page numbers and headers/footers from PDF."""
        new_lines = []
        for line in self.lines:
            line_strip = line.strip()

            # Skip page numbers (single digit/small numbers on their own line)
            if re.match(r'^\d{1,3}\s*$', line_strip) and len(line_strip) < 5:
                continue

            # Skip lines that look like page headers/footers with bullet points
            if re.match(r'^●.*[Tt]raining\s*$', line_strip):
                continue

            new_lines.append(line)

        self.lines = new_lines

    def fix_section_consistency(self):
        """Ensure consistent section structure."""
        new_lines = []
        for i, line in enumerate(self.lines):
            line_strip = line.strip()

            # Ensure "LESSON DEVELOPMENT" exists - add if missing after content starts
            if i > 0 and re.match(r'^####\s+[A-Z]\.\s+', line_strip):
                # Check if we're in lesson content (look back for objectives/assignments)
                has_objectives = any('LESSON OBJECTIVES' in l for l in self.lines[max(0, i-20):i])
                has_assignments = any('ASSIGNMENTS' in l for l in self.lines[max(0, i-20):i])

                if has_objectives and has_assignments:
                    # Check if LESSON DEVELOPMENT was already added
                    has_dev = any('LESSON DEVELOPMENT' in l for l in self.lines[max(0, i-5):i])
                    if not has_dev and i > 0 and self.lines[i-1].strip() == '':
                        new_lines.append("LESSON DEVELOPMENT")
                        new_lines.append("")

            new_lines.append(line)

        self.lines = new_lines

    def save(self, output_path: str | None = None):
        """Save cleaned markdown to file."""
        if output_path is None:
            output_path = self.file_path
        else:
            output_path = Path(output_path)

        output_path.write_text('\n'.join(self.lines), encoding='utf-8')
        print(f"✓ Cleaned: {output_path}")


def main():
    """Clean all course markdown files."""
    files = [
        "C:/Users/viren/source/jcbiblecourse/output/121 PHILS TEXT.md",
        "C:/Users/viren/source/jcbiblecourse/output/CL TEXT PHILS.md",
        "C:/Users/viren/source/jcbiblecourse/output/GALATIANS PHILS TEXT.md"
    ]

    for file_path in files:
        try:
            print(f"Cleaning {Path(file_path).name}...")
            cleaner = MarkdownCleaner(file_path)
            cleaned = cleaner.clean()

            # Save to _PARSING version (keeps original intact)
            output_file = file_path.replace('.md', '_PARSING.md')
            cleaner.save(output_file)

            # Count improvements
            original_lines = len(Path(file_path).read_text(encoding='utf-8').split('\n'))
            cleaned_lines = len(cleaned.split('\n'))
            removed = original_lines - cleaned_lines
            print(f"  ✓ Removed {removed} lines (TOC & artifacts)")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("\n✓ Generated *_PARSING.md files for parser input.")
    print("✓ Original .md files preserved with Table of Contents intact.")
    print("\nNext: python parse_courses_v2.py")

if __name__ == "__main__":
    main()
