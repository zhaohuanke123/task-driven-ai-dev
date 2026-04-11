---
name: task-driven-ai-dev
description: Turn a repository into a task-driven AI delivery loop with durable planning artifacts, guarded single-task execution, progress logging, and validation gates. Use when Codex needs to bootstrap or operate workflows built around files like architecture.md, task.json, progress.txt, project-config.json, CLAUDE.md, AGENTS.md, or similar backlog-driven harnesses, especially when replacing shell-based automation with explicit subagent orchestration.
---
# Task-Driven AI Dev

Use this skill to create or operate a repo-level AI development harness. Keep the loop explicit: define the system, choose one task, implement it, validate it, record evidence, then stop.

## Quick Start

1. Read the current artifact set. Prefer `architecture.md`, `task.json`, `progress.txt`, and `project-config.json` when they exist.
2. If the repo does not have those files, create them from `assets/templates/`.
3. Load `references/workflow-contract.md` before running an iteration.
4. Use `scripts/select_next_task.py` to choose the next ready task instead of scanning `passes: false` by hand.
5. Execute exactly one task unless the user explicitly asks for a broader phase.
6. Use `scripts/validate_iteration.py` before marking a task complete.

## Operating Modes

- Bootstrap a new repo: create the artifact set, define commands, and seed the first backlog.
- Run one delivery iteration: select one ready task, implement, test, update artifacts, and stop.
- Unblock a stuck repo: diagnose why a task cannot be safely completed, record the block, and stop without marking success.
- Harden the harness: tighten testing gates, task structure, and async-state handling after regressions.

## Core Workflow

### 1. Assess the repo state

- Identify whether the repo already has architecture, task, progress, and project-config artifacts.
- Identify the execution surface: app root, bootstrap commands, test commands, browser-test requirements, deployment blockers.
- Read recent git history to separate planned work from post-task bugfix work.

### 2. Normalize the artifact contract

- Keep one architecture document that explains the system and major constraints.
- Keep one task file that is the source of truth for backlog state.
- Keep one progress log with dated entries and explicit testing evidence.
- Keep one project-config file that tells future agents how to bootstrap and validate the repo.
- If a project also uses tool-specific memory files such as `CLAUDE.md` or `AGENTS.md`, treat them as adapters, not the canonical workflow definition.

See `references/artifact-model.md` for the detailed contract and template usage.

### 3. Select work conservatively

- Prefer one ready task with satisfied dependencies.
- Do not take a blocked task unless the user explicitly asks to unblock it.
- Do not bundle unrelated tasks only to reduce session count.
- When the backlog is complete and new defects appear, record them as explicit bugfix tasks or clearly separate them in progress history.

### 4. Decide: local or delegated?

Before implementing, check the task nature:

- **Research with multiple independent targets** → Launch parallel subagents (e.g., "research Cursor, Windsurf, and Continue UX")
- **Isolated implementation with clear scope** → Consider worker subagent
- **Tiny or tightly coupled to current context** → Stay local

See `references/subagent-orchestration.md` for recommended subagent roles (selection, worker, verification).

### 5. Execute one guarded iteration

- Bootstrap the environment only as needed.
- Implement the chosen task.
- Run the required validation commands.
- Do browser-driven validation when the task changes user-facing flows or core interactions.
- Update the task file and progress log only after the validation evidence is real.
- Stop after the task is complete or blocked.

See `references/workflow-contract.md` for the full iteration protocol.


## Guardrails

- Never mark a task complete without evidence in testing artifacts or commands.
- Never hide a block by flipping `passes` to `true`.
- Never rely on client-side polling alone for long-running async workflows; persist or recover state server-side when possible.
- Never assume a public URL works for private storage.
- Never let `progress.txt` become fiction; it is memory for future agents, not marketing copy.

Load `references/lessons-from-history.md` when hardening an existing harness or debugging regressions that appeared after the main backlog was finished.

## Bundled Resources

- `assets/templates/architecture.md`: starting point for the architecture contract.
- `assets/templates/task.json`: backlog template with dependencies, blocked state, and validation notes.
- `assets/templates/progress.txt`: durable progress and blocking log template.
- `assets/templates/project-config.json`: repo-specific command and artifact map.
- `scripts/select_next_task.py`: choose the next ready task deterministically.
- `scripts/validate_iteration.py`: validate task/progress consistency before completion.
- `references/workflow-contract.md`: one-task iteration protocol and done gate.
- `references/artifact-model.md`: artifact semantics and field expectations.
- `references/subagent-orchestration.md`: recommended subagent roles and delegation patterns.
- `references/lessons-from-history.md`: failure modes extracted from a real long-running AI-built repo.

## Output Expectations

- When bootstrapping, leave the repo with a coherent artifact set and explicit commands.
- When iterating, leave the repo with one completed task or one clearly documented block.
- When hardening, prefer small protocol changes that improve truthfulness and recoverability over flashy automation.
