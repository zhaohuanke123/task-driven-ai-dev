#!/usr/bin/env python3
"""
Validate that architecture.md has all required sections.

This script implements the "机械化执行" principle of Harness Engineering:
文档会腐烂，但 lint 规则不会。

Usage:
    python validate_architecture.py [--architecture-file architecture.md]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# 必需章节 - 缺少则报错
REQUIRED_SECTIONS = [
    "Overview",
    "Tech Stack",
    "Directory Structure",
    "Data Model",
    "API Design",
    "Key Constraints",
]

# 推荐章节 - 缺少则警告
RECOMMENDED_SECTIONS = [
    "Environment Variables",
    "Key Design Decisions",
]


def load_architecture(path: Path) -> str:
    """Load architecture.md content."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: architecture.md not found: {path}") from exc


def extract_sections(content: str) -> set[str]:
    """Extract all ## headings from the document."""
    pattern = r"^## (.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)
    return {m.strip() for m in matches}


def validate_sections(content: str) -> tuple[list[str], list[str]]:
    """Validate required and recommended sections."""
    sections = extract_sections(content)

    missing_required = []
    missing_recommended = []

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            missing_required.append(section)

    for section in RECOMMENDED_SECTIONS:
        if section not in sections:
            missing_recommended.append(section)

    return missing_required, missing_recommended


def validate_tech_stack_format(content: str) -> list[str]:
    """Validate Tech Stack section has proper table format."""
    errors = []

    # Check if Tech Stack section exists and has a table
    tech_stack_match = re.search(
        r"^## Tech Stack\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL
    )

    if tech_stack_match:
        section_content = tech_stack_match.group(1)
        # Look for table format (| Layer | Technology |)
        if "|" not in section_content:
            errors.append("Tech Stack section should use table format with | columns")
        # Check for required columns
        if "Layer" not in section_content or "Technology" not in section_content:
            errors.append("Tech Stack table should have 'Layer' and 'Technology' columns")

    return errors


def validate_key_constraints(content: str) -> list[str]:
    """Validate Key Constraints section has content."""
    errors = []

    constraints_match = re.search(
        r"^## Key Constraints\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL
    )

    if constraints_match:
        section_content = constraints_match.group(1).strip()
        # Check if section has actual content (not just comments)
        non_comment_lines = [
            line for line in section_content.split("\n")
            if line.strip() and not line.strip().startswith("<!--") and not line.strip().startswith("-->")
        ]
        if len(non_comment_lines) < 2:
            errors.append("Key Constraints section appears empty - must define constraints")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture-file",
        default="architecture.md",
        help="Path to architecture.md"
    )
    args = parser.parse_args()

    content = load_architecture(Path(args.architecture_file))

    missing_required, missing_recommended = validate_sections(content)
    format_errors = validate_tech_stack_format(content)
    constraint_errors = validate_key_constraints(content)

    exit_code = 0

    if missing_required:
        print("ERROR: Missing required sections:")
        for section in missing_required:
            print(f"  - {section}")
        print("\nRequired sections are:")
        for section in REQUIRED_SECTIONS:
            print(f"  - {section}")
        exit_code = 1

    if missing_recommended:
        print("WARNING: Missing recommended sections:")
        for section in missing_recommended:
            print(f"  - {section}")

    if format_errors:
        print("ERROR: Format issues:")
        for error in format_errors:
            print(f"  - {error}")
        exit_code = 1

    if constraint_errors:
        print("ERROR: Constraint issues:")
        for error in constraint_errors:
            print(f"  - {error}")
        exit_code = 1

    if exit_code == 0:
        print("OK: architecture.md passes validation")
        print(f"  - Found {len(extract_sections(content))} sections")
        print("  - All required sections present")
        print("  - Format checks passed")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
