#!/usr/bin/env python3
"""
Complete PDF → Markdown → JSON pipeline for course materials.
Orchestrates three steps: PDF extraction, markdown cleanup, content parsing.
"""

import subprocess
import sys
from pathlib import Path


def run_pipeline(project_root: str = ".") -> bool:
    """Execute the complete pipeline."""
    project_path = Path(project_root).resolve()
    script_dir = Path(__file__).parent

    print(f"\n{'='*70}")
    print("COURSE MATERIAL PIPELINE: PDF → Markdown → Cleaned → JSON")
    print(f"{'='*70}")
    print(f"Project root: {project_path}\n")

    # Step 1: Convert PDFs to Markdown
    print("[STEP 1] Converting PDFs to Markdown...")
    result = subprocess.run(
        [sys.executable, str(script_dir / "pdf_to_markdown.py"), str(project_path)],
        cwd=str(project_path)
    )
    if result.returncode != 0:
        print("✗ PDF conversion failed")
        return False

    # Step 2: Clean up Markdown files
    print("\n[STEP 2] Cleaning up Markdown files...")
    result = subprocess.run(
        [sys.executable, str(script_dir / "cleanup_markdown.py"), str(project_path)],
        cwd=str(project_path)
    )
    if result.returncode != 0:
        print("✗ Markdown cleanup failed")
        return False

    # Step 3: Parse to JSON
    print("\n[STEP 3] Parsing Markdown to JSON...")
    result = subprocess.run(
        [sys.executable, str(script_dir / "parse_courses_v2.py"), str(project_path)],
        cwd=str(project_path)
    )
    if result.returncode != 0:
        print("✗ Parsing failed")
        return False

    # Print summary
    print(f"\n{'='*70}")
    print("PIPELINE COMPLETE ✓")
    print(f"{'='*70}")
    print(f"Output folders:")
    print(f"  Markdown: {project_path}/output/")
    print(f"  JSON: {project_path}/data/")
    print(f"\nOriginal markdown with TOC preserved for reference")
    print(f"_PARSING.md files show where content cleaning occurred")

    return True


def main():
    """Main entry point."""
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    success = run_pipeline(project_root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
