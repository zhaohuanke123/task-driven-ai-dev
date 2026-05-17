# Coding Workflow

A structured development workflow skill for Claude Code with PEV (Plan-Execute-Verify) three-layer agent architecture.

## Overview

This skill implements a task-driven development workflow with three specialized AI agents:

- **Planner** — Analyzes codebase and requirements, generates implementation plans with file ownership maps, acceptance criteria, and test scenarios
- **Executor** — Implements code according to the Planner's plan in isolated worktrees
- **Verifier** — Independently writes tests, runs full test suites, and audits docs/code/tests consistency

Key principles:
- **Plan-Execute-Verify separation** — Planning, coding, and testing are done by independent agents to combat optimistic bias
- **GAN-like architecture** — Generator (executor) and discriminator (verifier) are physically isolated
- **File ownership** — Each file has exactly one owner; no two agents modify the same file
- **Feedback loop** — Verifier failures are sent back to executor with specific fix suggestions (max 2 retries)

## Installation

```bash
python install.py --target <project-dir> --name "Project Name" \
  --description "Brief description" \
  --tech-frontend "React+TypeScript+Tailwind" \
  --tech-backend "Node.js" \
  --tech-database "PostgreSQL"
```

Deploys project files and PEV agent definitions to the target project:

**Project files (4):**
- `CLAUDE.md` — Navigation entry point
- `architecture.md` — Tech stack, directory structure, constraints
- `task.json` — Task definitions and dependencies
- `progress.txt` — Progress log and test evidence

**PEV Agent definitions (3):**
- `.agents/planner.md` — Plan layer: analyzes requirements, generates implementation plans
- `.agents/executor.md` — Execute layer: implements code per plan
- `.agents/verifier.md` — Verify layer: writes tests, runs independent review

## Quick Start

1. **Initialize your project** with the required files (see Installation above)

2. **Define your tasks** in `task.json`:

```json
{
  "project": "My Project",
  "description": "A fullstack application",
  "tasks": [
    {
      "id": 1,
      "title": "Setup Environment",
      "description": "Initialize project structure",
      "steps": ["Create package.json", "Setup TypeScript", "Configure Tailwind"],
      "dependencies": [],
      "done": false,
      "docs": "docs/requirements.md#FR-001"
    }
  ]
}
```

3. **Invoke the skill**:

```
/coding-workflow
```

## PEV Architecture

```
Orchestrator (SKILL.md)
    │
    ▼
┌─ Layer 1: Planner ─────────────────────┐
│  Analyze codebase + requirements        │
│  Output: Implementation Plan            │
│  + File Ownership + Test Scenarios      │
│  Permission: read-only                  │
└────────────────────────────────────────┘
    │ ready
    ▼
┌─ Layer 2: Executor ────────────────────┐
│  Write code per Planner's plan          │
│  in isolated worktree                   │
│  Validation: lint + build only          │
└────────────────────────────────────────┘
    │ completed
    ▼
┌─ Layer 3: Verifier ────────────────────┐
│  Write tests + run tests                │
│  + independent review                   │
│  FAIL → send fix suggestions to executor│
└────────────────────────────────────────┘
    │ PASS → merge | FAIL → retry (max 2)
```

## Usage

### Continue Development

```
/coding-workflow
```

The agent will:
1. Read `task.json` and `progress.txt`
2. Select the next incomplete task
3. Pass the Documentation Gate
4. **PEV Flow**: Spawn Planner → Executor → Verifier
5. Handle verifier feedback (retry if needed)
6. Merge and commit on PASS

### Check Status

```
/coding-workflow status
```

### Work on Specific Task

```
/coding-workflow task 5
```

## Agent Definitions

| Agent | File | Layer | Tools | Writes Files |
|-------|------|-------|-------|-------------|
| Planner | `.agents/planner.md` | Plan | Read, Bash, Grep, Glob | No (read-only) |
| Executor | `.agents/executor.md` | Execute | Read, Write, Edit, Bash, Grep, Glob, TodoWrite | Implementation files only |
| Verifier | `.agents/verifier.md` | Verify | Read, Write, Edit, Bash, Grep, Glob | Test files only |

> Agent definitions are stored in `skills/coding-workflow/assets/agents/` and deployed to `.agents/` by `install.py`.

## Orchestration Flow (10 Steps)

1. **Task Selection** — Pick next task from `task.json`
2. **Documentation Gate** — Verify docs exist before code changes
3. **Worktree Creation** — Isolated git worktree per task
4. **Spawn Planner** — Analyze and generate implementation plan
5. **Handle Planner Result** — `ready` → proceed, `blocked` → report
6. **Spawn Executor** — Implement per plan (lint + build only)
7. **Handle Executor Result** — `completed` → verify, `blocked` → report
8. **Spawn Verifier** — Write tests, run tests, independent review
9. **Handle Verifier Result** — PASS → merge; FAIL → retry (max 2 rounds)
10. **Commit** — Update `task.json` and `progress.txt`

## Project Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Navigation entry point (auto-loaded) |
| `architecture.md` | Tech stack, directory structure, constraints |
| `task.json` | Task definitions and dependencies |
| `progress.txt` | Development history, test evidence, blocks |
| `docs/requirements.md` | Behavior and scope requirements |
| `docs/design.md` | Module design and contracts |

## Memory Rules

Memory is routing, not state. When memory conflicts with repo files, trust repo files:

```
User's latest explicit instruction
> PROJECT.md / docs/* / task.json / progress.txt
> CLAUDE.md / architecture.md
> skill instructions
> memory hints
```

## Scripts

### validate_architecture.py

```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

Checks `architecture.md` for all required sections.

## License

Apache-2.0
