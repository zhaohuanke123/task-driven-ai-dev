#!/usr/bin/env python3
"""
Select the next task to work on from task.json.
Prioritizes by: passes status, priority field, dependencies.

Usage:
    python select_next_task.py [--task-file task.json] [--format text|json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def load_task_file(path: Path) -> dict[str, Any]:
    """Load task.json file."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"task file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse JSON from {path}: {exc}") from exc


def build_indexes(tasks: list[dict[str, Any]]) -> tuple[dict[Any, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Build indexes for quick task lookup."""
    by_id: dict[Any, dict[str, Any]] = {}
    by_title: dict[str, dict[str, Any]] = {}
    for task in tasks:
        if "id" in task:
            by_id[task["id"]] = task
        title = str(task.get("title", "")).strip()
        if title:
            by_title[title] = task
    return by_id, by_title


def dependency_satisfied(task: dict[str, Any], by_id: dict[Any, dict[str, Any]], by_title: dict[str, dict[str, Any]]) -> bool:
    """Check if all dependencies are satisfied."""
    for dependency in task.get("dependencies", []):
        dependency_task = by_id.get(dependency) or by_title.get(str(dependency))
        if dependency_task is None or not dependency_task.get("passes", False):
            return False
    return True


def priority_key(value: Any) -> tuple[int, int]:
    """Get sort key for priority value."""
    if isinstance(value, (int, float)):
        return (0, int(value))
    if isinstance(value, str):
        return (1, PRIORITY_ORDER.get(value.lower(), 99))
    return (9, 0)


def task_sort_key(item: tuple[int, dict[str, Any]]) -> tuple[tuple[int, int], int, int]:
    """Get sort key for task."""
    index, task = item
    task_id = task.get("id")
    normalized_id = task_id if isinstance(task_id, int) else index
    return (priority_key(task.get("priority")), index, normalized_id)


def select_task(tasks: list[dict[str, Any]], allow_blocked: bool) -> tuple[dict[str, Any] | None, str]:
    """Select the next ready task."""
    by_id, by_title = build_indexes(tasks)
    remaining: list[tuple[int, dict[str, Any]]] = []
    blocked: list[dict[str, Any]] = []
    waiting: list[dict[str, Any]] = []

    for index, task in enumerate(tasks):
        if task.get("passes", False):
            continue
        if task.get("blocked", False) and not allow_blocked:
            blocked.append(task)
            continue
        if not dependency_satisfied(task, by_id, by_title):
            waiting.append(task)
            continue
        remaining.append((index, task))

    if remaining:
        remaining.sort(key=task_sort_key)
        return remaining[0][1], "ready"
    if waiting:
        return None, "waiting_for_dependencies"
    if blocked:
        return None, "all_remaining_tasks_blocked"
    return None, "no_incomplete_tasks"


def print_text(task: dict[str, Any] | None, reason: str) -> None:
    """Print task in text format."""
    if task is None:
        print(f"selection: {reason}")
        return

    print(f"selection: {reason}")
    print(f"id: {task.get('id', '')}")
    print(f"title: {task.get('title', '')}")
    print(f"description: {task.get('description', '')}")
    print(f"requirement_ref: {task.get('requirement_ref', '')}")
    print(f"design_ref: {task.get('design_ref', '')}")
    print(f"docs_updated: {task.get('docs_updated', False)}")
    print(f"implementation_done: {task.get('implementation_done', False)}")
    print(f"verified: {task.get('verified', False)}")
    dependencies = task.get("dependencies", [])
    print(f"dependencies: {dependencies if dependencies else '[]'}")
    print("steps:")
    for step in task.get("steps", []):
        print(f"- {step}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", default="task.json", help="Path to task.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--allow-blocked", action="store_true", help="Allow blocked tasks to be selected")
    args = parser.parse_args()

    payload = load_task_file(Path(args.task_file))
    tasks = payload.get("tasks")
    if not isinstance(tasks, list):
        raise SystemExit("task file must contain a top-level 'tasks' array")

    selected, reason = select_task(tasks, allow_blocked=args.allow_blocked)

    if args.format == "json":
        print(json.dumps({"selection": reason, "task": selected}, ensure_ascii=False, indent=2))
    else:
        print_text(selected, reason)

    return 0 if selected is not None else 2


if __name__ == "__main__":
    sys.exit(main())
