#!/usr/bin/env python3
"""Validate backlog and progress consistency for one task-driven iteration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"missing text file: {path}") from exc


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def find_task(tasks: list[dict[str, Any]], task_id: str | None, task_title: str | None) -> dict[str, Any] | None:
    for task in tasks:
        if task_id is not None and str(task.get("id")) == task_id:
            return task
        if task_title is not None and normalize(str(task.get("title", ""))) == normalize(task_title):
            return task
    return None


def progress_mentions_task(progress_text: str, task: dict[str, Any]) -> bool:
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


def validate_dependencies(tasks: list[dict[str, Any]]) -> list[str]:
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
    errors: list[str] = []
    if task.get("passes", False) and task.get("blocked", False):
        errors.append("task cannot be both passed and blocked")
    if task.get("passes", False) and not progress_mentions_task(progress_text, task):
        errors.append("passed task is not mentioned in progress log")
    if not isinstance(task.get("steps", []), list) or not task.get("steps"):
        errors.append("task must include a non-empty steps array")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", default="task.json", help="Path to task.json")
    parser.add_argument("--progress-file", default="progress.txt", help="Path to progress.txt")
    parser.add_argument("--task-id", help="Task id to validate")
    parser.add_argument("--task-title", help="Task title to validate")
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

    if target_task is not None:
        print(f"OK: task {target_task.get('id', '')} passed validation checks")
    else:
        print("OK: task file and progress log passed validation checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
