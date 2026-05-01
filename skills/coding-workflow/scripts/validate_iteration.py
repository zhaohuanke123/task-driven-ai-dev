#!/usr/bin/env python3
"""
Validate backlog and progress consistency for one coding-workflow iteration.

Usage:
    python validate_iteration.py [--task-file task.json] [--progress-file progress.txt] [--task-id ID]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON file."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def load_text(path: Path) -> str:
    """Load text file."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"missing text file: {path}") from exc


def normalize(value: str) -> str:
    """Normalize string for comparison."""
    return re.sub(r"\s+", " ", value).strip().lower()


def find_task(tasks: list[dict[str, Any]], task_id: str | None, task_title: str | None) -> dict[str, Any] | None:
    """Find task by ID or title."""
    for task in tasks:
        if task_id is not None and str(task.get("id")) == task_id:
            return task
        if task_title is not None and normalize(str(task.get("title", ""))) == normalize(task_title):
            return task
    return None


def progress_mentions_task(progress_text: str, task: dict[str, Any]) -> bool:
    """Check if progress.txt mentions the task."""
    title = str(task.get("title", "")).strip()
    task_id = task.get("id")
    probes = []
    if title:
        probes.append(title)
    if task_id is not None:
        probes.append(f"Task {task_id}")
        probes.append(f"Task: {task_id}")
        probes.append(f"Task {task_id}:")
    normalized_progress = normalize(progress_text)
    return any(normalize(probe) in normalized_progress for probe in probes)


def progress_mentions_documentation_skip(progress_text: str, task: dict[str, Any]) -> bool:
    """Check if progress.txt records an explicit documentation skip for the task."""
    normalized_progress = normalize(progress_text)
    if "documentation skip" not in normalized_progress and "docs updated: skipped" not in normalized_progress:
        return False
    return progress_mentions_task(progress_text, task)


def validate_dependencies(tasks: list[dict[str, Any]]) -> list[str]:
    """Validate task dependencies."""
    errors: list[str] = []
    known_ids = {task.get("id") for task in tasks if "id" in task}
    known_titles = {str(task.get("title", "")).strip() for task in tasks}
    for task in tasks:
        for dependency in task.get("dependencies", []):
            if dependency not in known_ids and str(dependency).strip() not in known_titles:
                errors.append(
                    f"task {task.get('id', '?')} references unknown dependency {dependency!r}"
                )
    return errors


def validate_task(progress_text: str, task: dict[str, Any]) -> list[str]:
    """Validate a single task."""
    errors: list[str] = []
    for field in ("requirement_ref", "design_ref", "docs_updated", "implementation_done", "verified"):
        if field not in task:
            errors.append(f"task must include {field!r} for documentation-gated workflow")
    for field in ("requirement_ref", "design_ref"):
        if field in task and not str(task.get(field, "")).strip():
            errors.append(f"task must include a non-empty {field!r}")
    if task.get("passes", False) and task.get("blocked", False):
        errors.append("task cannot be both passed and blocked")
    if task.get("passes", False) and not progress_mentions_task(progress_text, task):
        errors.append("passed task is not mentioned in progress log")
    if task.get("passes", False) and not task.get("implementation_done", False):
        errors.append("passed task must have implementation_done=true")
    if task.get("passes", False) and not task.get("verified", False):
        errors.append("passed task must have verified=true")
    if task.get("passes", False) and not task.get("docs_updated", False):
        if not progress_mentions_documentation_skip(progress_text, task):
            errors.append("passed task must have docs_updated=true or an explicit documentation skip in progress log")
    if not isinstance(task.get("steps", []), list) or not task.get("steps"):
        errors.append("task must include a non-empty steps array")
    return errors


def run_command(command: list[str], cwd: str) -> tuple[bool, str]:
    """Run a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, f"Command not found: {command[0]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", default="task.json", help="Path to task.json")
    parser.add_argument("--progress-file", default="progress.txt", help="Path to progress.txt")
    parser.add_argument("--task-id", help="Task id to validate")
    parser.add_argument("--task-title", help="Task title to validate")
    parser.add_argument("--project-dir", default=".", help="Project directory for running lint/build")
    parser.add_argument("--skip-lint", action="store_true", help="Skip lint check")
    parser.add_argument("--skip-build", action="store_true", help="Skip build check")
    args = parser.parse_args()

    task_payload = load_json(Path(args.task_file))
    progress_text = load_text(Path(args.progress_file))
    tasks = task_payload.get("tasks")
    if not isinstance(tasks, list):
        raise SystemExit("task file must contain a top-level 'tasks' array")

    errors = validate_dependencies(tasks)
    target_task: dict[str, Any] | None = None
    if args.task_id or args.task_title:
        target_task = find_task(tasks, args.task_id, args.task_title)
        if target_task is None:
            raise SystemExit("requested task was not found")
        errors.extend(validate_task(progress_text, target_task))
    else:
        for task in tasks:
            errors.extend(validate_task(progress_text, task))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    # Run lint and build checks
    lint_passed = True
    build_passed = True

    if not args.skip_lint and Path(f"{args.project_dir}/package.json").exists():
        print("Running lint...")
        lint_passed, lint_output = run_command(["npm", "run", "lint"], args.project_dir)
        if not lint_passed:
            print(f"LINT FAILED:\n{lint_output}")
        else:
            print("LINT PASSED")

    if not args.skip_build and Path(f"{args.project_dir}/package.json").exists():
        print("Running build...")
        build_passed, build_output = run_command(["npm", "run", "build"], args.project_dir)
        if not build_passed:
            print(f"BUILD FAILED:\n{build_output}")
        else:
            print("BUILD PASSED")

    if target_task is not None:
        print(f"OK: task {target_task.get('id', '')} passed validation checks")
    else:
        print("OK: task file and progress log passed validation checks")

    if not lint_passed or not build_passed:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
