#!/usr/bin/env python3
"""
Analyze task.json and group parallelizable tasks into execution batches.

Tasks in the same batch have no dependencies on each other and no declared
file conflicts, so they can be executed in parallel by separate subagents
each working in their own git worktree.

Usage:
    python plan_batches.py [--task-file task.json] [--format text|json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_task_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"task file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse JSON from {path}: {exc}") from exc


def build_task_map(tasks: list[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
    return {t["id"]: t for t in tasks if "id" in t}


def ready_tasks(tasks: list[dict[str, Any]], task_map: dict[Any, dict[str, Any]]) -> list[dict[str, Any]]:
    """Return tasks whose dependencies are all passed and that are not yet done."""
    result = []
    for task in tasks:
        if task.get("passes", False):
            continue
        if task.get("blocked", False):
            continue
        deps = task.get("dependencies", [])
        if all(
            task_map.get(dep, {}).get("passes", False)
            for dep in deps
        ):
            result.append(task)
    return result


def file_sets_overlap(a: list[str], b: list[str]) -> bool:
    """Check if two file lists share any path prefix (directory-level overlap)."""
    set_a = {p.rstrip("/").split("/")[0] if "/" in p else p for p in a}
    set_b = {p.rstrip("/").split("/")[0] if "/" in p else p for p in b}
    return bool(set_a & set_b)


def conflict_group_match(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Check if two tasks share a conflict_group."""
    groups_a = set(a.get("conflict_groups", []))
    groups_b = set(b.get("conflict_groups", []))
    return bool(groups_a & groups_b)


def has_conflict(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Determine if two tasks cannot safely run in parallel."""
    files_a = a.get("files", [])
    files_b = b.get("files", [])
    if files_a and files_b and file_sets_overlap(files_a, files_b):
        return True
    if conflict_group_match(a, b):
        return True
    return False


def assign_batches(tasks: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """
    Group ready tasks into parallel batches using a greedy algorithm.

    Tasks in the same batch are guaranteed to have no file-level conflicts
    with each other. Tasks with conflicts are pushed to separate batches
    (still parallel, just in different waves).
    """
    batches: list[list[dict[str, Any]]] = []
    remaining = list(tasks)

    while remaining:
        batch: list[dict[str, Any]] = []
        deferred: list[dict[str, Any]] = []

        for task in remaining:
            if any(has_conflict(task, member) for member in batch):
                deferred.append(task)
            else:
                batch.append(task)

        if batch:
            batches.append(batch)
        if not batch or not deferred:
            break
        remaining = deferred

    return batches


def format_batches(batches: list[list[dict[str, Any]]]) -> dict[str, Any]:
    output: dict[str, Any] = {"batches": []}
    for i, batch in enumerate(batches, 1):
        batch_info: dict[str, Any] = {
            "batch_id": i,
            "parallel_count": len(batch),
            "tasks": [],
        }
        for task in batch:
            tid = task["id"]
            batch_info["tasks"].append({
                "id": tid,
                "title": task.get("title", ""),
                "description": task.get("description", ""),
                "steps": task.get("steps", []),
                "requirement_ref": task.get("requirement_ref", ""),
                "design_ref": task.get("design_ref", ""),
                "docs_updated": task.get("docs_updated", False),
                "implementation_done": task.get("implementation_done", False),
                "verified": task.get("verified", False),
                "branch": f"feature/task-{tid}",
                "worktree": f".worktrees/task-{tid}",
                "files": task.get("files", []),
            })
        output["batches"].append(batch_info)
    return output


def print_text(output: dict[str, Any]) -> None:
    for batch in output["batches"]:
        print(f"\n=== Batch {batch['batch_id']} ({batch['parallel_count']} parallel tasks) ===")
        for task in batch["tasks"]:
            print(f"  Task #{task['id']}: {task['title']}")
            print(f"    Branch:   {task['branch']}")
            print(f"    Worktree: {task['worktree']}")
            print(f"    Requirement: {task['requirement_ref'] or '[missing]'}")
            print(f"    Design:      {task['design_ref'] or '[missing]'}")
            print(f"    Docs updated: {task['docs_updated']}")
            if task["files"]:
                print(f"    Files:    {', '.join(task['files'])}")
            for step in task["steps"]:
                print(f"    - {step}")
    total = sum(b["parallel_count"] for b in output["batches"])
    print(f"\nTotal: {total} tasks in {len(output['batches'])} batch(es)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", default="task.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--max-parallel", type=int, default=0,
        help="Cap parallel tasks per batch (0 = unlimited)",
    )
    args = parser.parse_args()

    payload = load_task_file(Path(args.task_file))
    tasks = payload.get("tasks")
    if not isinstance(tasks, list):
        raise SystemExit("task file must contain a top-level 'tasks' array")

    task_map = build_task_map(tasks)
    eligible = ready_tasks(tasks, task_map)

    if not eligible:
        print("No tasks ready for execution.")
        return 0

    batches = assign_batches(eligible)

    if args.max_parallel > 0:
        capped: list[list[dict[str, Any]]] = []
        for batch in batches:
            for i in range(0, len(batch), args.max_parallel):
                capped.append(batch[i : i + args.max_parallel])
        batches = capped

    output = format_batches(batches)

    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_text(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
