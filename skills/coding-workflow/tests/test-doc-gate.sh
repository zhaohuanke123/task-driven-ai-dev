#!/usr/bin/env bash
# test-doc-gate.sh — Simulate PreToolUse hook environment and test doc-gate.sh
#
# Creates a temp project with git repo, task.json, progress.txt,
# then pipes JSON to doc-gate.sh and checks exit codes.
#
# Usage: bash tests/test-doc-gate.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOK="$SCRIPT_DIR/../assets/hooks/doc-gate.sh"
PASS=0
FAIL=0
TOTAL=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# --- Helpers ---

assert_exit() {
  local desc="$1" expected="$2" actual="$3"
  TOTAL=$((TOTAL + 1))
  if [ "$actual" -eq "$expected" ]; then
    printf "${GREEN}PASS${NC} [%d] %s (exit=%d)\n" "$TOTAL" "$desc" "$actual"
    PASS=$((PASS + 1))
  else
    printf "${RED}FAIL${NC} [%d] %s — expected exit=%d, got exit=%d\n" "$TOTAL" "$desc" "$expected" "$actual"
    FAIL=$((FAIL + 1))
  fi
}

make_input() {
  local file="$1"
  printf '{"tool_name":"Edit","input":{"file_path":"%s","old_string":"x","new_string":"y"}}' "$file"
}

# --- Setup: temp project dir ---

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "=== Test dir: $TMPDIR ==="
echo ""

# Init git repo
cd "$TMPDIR"
git init -q
git config user.email "test@test.com"
git config user.name "Test"

# Create initial commit so HEAD exists
echo "# My Project" > README.md
git add README.md
git commit -qm "init"

# Create task.json with active tasks
cat > task.json << 'TASKJSON'
{
  "project": "Test Project",
  "tasks": [
    {
      "id": 1,
      "title": "Setup",
      "status": "completed",
      "steps": ["Init project"],
      "dependencies": [],
      "done": true
    },
    {
      "id": 2,
      "title": "Add feature",
      "status": "in_progress",
      "steps": ["Implement feature"],
      "dependencies": [1],
      "done": false
    }
  ]
}
TASKJSON

# Create empty progress.txt
touch progress.txt

echo "--- Running tests ---"
echo ""

# ==========================================
# Test 1: Edit source file — no doc changes → BLOCKED
# ==========================================
make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "source file, no docs → blocked" 2 $?

# ==========================================
# Test 2: Edit non-source file → ALLOW
# ==========================================
make_input "docs/design.md" | bash "$HOOK" 2>/dev/null
assert_exit "docs file → allow" 0 $?

make_input "architecture.md" | bash "$HOOK" 2>/dev/null
assert_exit "architecture.md → allow" 0 $?

make_input "package.json" | bash "$HOOK" 2>/dev/null
assert_exit "config file → allow" 0 $?

make_input "tests/main.test.ts" | bash "$HOOK" 2>/dev/null
assert_exit "test file → allow" 0 $?

make_input "src/app/main.test.ts" | bash "$HOOK" 2>/dev/null
assert_exit "test file in src → allow" 0 $?

# ==========================================
# Test 3: Source file + doc changed in git diff → ALLOW
# ==========================================
mkdir -p docs
echo "# Design" > docs/design.md
git add docs/design.md

make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "source file, docs in git diff → allow" 0 $?

# Reset for next test
git reset HEAD docs/design.md >/dev/null 2>&1
rm -f docs/design.md

# ==========================================
# Test 4: Source file + BYPASS in progress.txt → ALLOW
# ==========================================
echo "[DOC-GATE-BYPASS] bug fix, docs already correct" > progress.txt

make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "source file, BYPASS in progress.txt → allow" 0 $?

# ==========================================
# Test 5: Source file + stale BYPASS (no current BYPASS) → BLOCKED
# ==========================================
echo "# Old progress" > progress.txt
echo "Something happened" >> progress.txt

make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "source file, no BYPASS, no docs → blocked" 2 $?

# ==========================================
# Test 6: No task.json → hook inactive, ALLOW
# ==========================================
rm task.json

make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "no task.json → allow (hook inactive)" 0 $?

# Restore task.json
cat > task.json << 'TASKJSON'
{
  "project": "Test Project",
  "tasks": [
    {
      "id": 1,
      "title": "Setup",
      "status": "completed",
      "steps": ["Init project"],
      "dependencies": [],
      "done": true
    },
    {
      "id": 2,
      "title": "Add feature",
      "status": "in_progress",
      "steps": ["Implement feature"],
      "dependencies": [1],
      "done": false
    }
  ]
}
TASKJSON

# ==========================================
# Test 7: All tasks completed → ALLOW
# ==========================================
cat > task.json << 'TASKJSON'
{
  "project": "Test Project",
  "tasks": [
    {
      "id": 1,
      "title": "Setup",
      "status": "completed",
      "steps": ["Init project"],
      "dependencies": [],
      "done": true
    },
    {
      "id": 2,
      "title": "Add feature",
      "status": "completed",
      "steps": ["Implement feature"],
      "dependencies": [1],
      "done": true
    }
  ]
}
TASKJSON

make_input "src/app/main.ts" | bash "$HOOK" 2>/dev/null
assert_exit "all tasks completed → allow" 0 $?

# Restore active task.json
cat > task.json << 'TASKJSON'
{
  "project": "Test Project",
  "tasks": [
    {
      "id": 1,
      "title": "Setup",
      "status": "completed",
      "steps": ["Init project"],
      "dependencies": [],
      "done": true
    },
    {
      "id": 2,
      "title": "Add feature",
      "status": "in_progress",
      "steps": ["Implement feature"],
      "dependencies": [1],
      "done": false
    }
  ]
}
TASKJSON

# ==========================================
# Test 8: Blocked message contains helpful info
# ==========================================
echo "" > progress.txt

output=$(make_input "src/app/main.ts" | bash "$HOOK" 2>&1)
exit_code=$?
assert_exit "blocked returns exit 2" 2 $exit_code

if echo "$output" | grep -q "BLOCKED"; then
  printf "${GREEN}PASS${NC} [extra] blocked message contains 'BLOCKED'\n"
  PASS=$((PASS + 1))
else
  printf "${RED}FAIL${NC} [extra] blocked message missing 'BLOCKED'\n"
  FAIL=$((FAIL + 1))
fi
TOTAL=$((TOTAL + 1))

if echo "$output" | grep -q "DOC-GATE-BYPASS"; then
  printf "${GREEN}PASS${NC} [extra] blocked message shows bypass instructions\n"
  PASS=$((PASS + 1))
else
  printf "${RED}FAIL${NC} [extra] blocked message missing bypass instructions\n"
  FAIL=$((FAIL + 1))
fi
TOTAL=$((TOTAL + 1))

# ==========================================
# Test 9: Various source paths
# ==========================================
echo "" > progress.txt

make_input "lib/utils.ts" | bash "$HOOK" 2>/dev/null
assert_exit "lib/ path → blocked" 2 $?

make_input "app/index.ts" | bash "$HOOK" 2>/dev/null
assert_exit "app/ path → blocked" 2 $?

make_input "internal/service.go" | bash "$HOOK" 2>/dev/null
assert_exit "internal/ path → blocked" 2 $?

make_input "frontend/src/App.tsx" | bash "$HOOK" 2>/dev/null
assert_exit "frontend/src/ path → blocked" 2 $?

# ==========================================
# Summary
# ==========================================
echo ""
echo "=========================="
printf "Results: ${GREEN}%d passed${NC}, ${RED}%d failed${NC}, %d total\n" "$PASS" "$FAIL" "$TOTAL"
echo "=========================="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
