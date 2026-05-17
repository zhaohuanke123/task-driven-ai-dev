#!/usr/bin/env bash
# doc-gate.sh — PreToolUse Hook for Documentation Gate enforcement
#
# Blocks source code edits when no documentation has been updated.
# Bypass: write "[DOC-GATE-BYPASS] Task #<id>: <reason>" in progress.txt
#
# Exit codes: 0 = allow, 2 = block (with message to stderr)

set -euo pipefail

# --- Read tool input from stdin ---
input=$(cat)

# --- Extract file_path from JSON ---
# Handles both "file_path" and "path" keys
file_path=$(echo "$input" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
if [ -z "$file_path" ]; then
  file_path=$(echo "$input" | sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
fi

# No file path found — not a file-editing tool, allow
if [ -z "$file_path" ]; then
  exit 0
fi

# Normalize path
file_path="${file_path#./}"

# --- Is this a source code file? ---
is_source=false
case "$file_path" in
  src/*|lib/*|app/*|pkg/*|internal/*|cmd/*|server/*|pages/*|components/*)
    # Exclude test files
    case "$file_path" in
      *.test.*|*.spec.*|*__tests__*|*/test/*|*/tests/*)
        ;;
      *)
        is_source=true
        ;;
    esac
    ;;
esac

if [ "$is_source" = false ]; then
  exit 0
fi

# --- Check: no task.json → hook not active ---
if [ ! -f "task.json" ]; then
  exit 0
fi

# --- Find current task ID from task.json ---
# First task with done=false and all dependencies satisfied
current_task_id=$(python3 -c "
import json, sys
try:
    data = json.load(open('task.json', encoding='utf-8'))
    done_ids = {t['id'] for t in data.get('tasks', []) if t.get('done')}
    for t in data.get('tasks', []):
        if not t.get('done') and all(d in done_ids for d in t.get('dependencies', [])):
            print(t['id'])
            break
except Exception:
    pass
" 2>/dev/null || true)

# No current task → not active
if [ -z "$current_task_id" ]; then
  exit 0
fi

# --- Check 1: git diff has documentation changes ---
has_doc_changes=false
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  changed_files=$(git diff --name-only HEAD 2>/dev/null || true)
  for f in $changed_files; do
    case "$f" in
      docs/*|*.md|CLAUDE.md|architecture.md|requirements*|design*)
        has_doc_changes=true
        break
        ;;
    esac
  done
fi

if [ "$has_doc_changes" = true ]; then
  exit 0
fi

# --- Check 2: BYPASS in progress.txt for current task ---
has_bypass=false
if [ -f "progress.txt" ]; then
  if grep -q "\[DOC-GATE-BYPASS\] Task #$current_task_id:" progress.txt 2>/dev/null; then
    has_bypass=true
  fi
fi

if [ "$has_bypass" = true ]; then
  exit 0
fi

# --- Block ---
{
  echo ""
  echo "## Documentation Gate: BLOCKED ##"
  echo "Refusing to edit source file: $file_path"
  echo ""
  echo "Documentation Gate requires updating docs before modifying source code."
  echo ""
  echo "Options to proceed:"
  echo "  1. Edit a documentation file first (docs/*, *.md), then retry"
  echo "  2. Add a bypass entry in progress.txt:"
  echo "     [DOC-GATE-BYPASS] Task #$current_task_id: <reason>"
  echo ""
} >&2

exit 2
