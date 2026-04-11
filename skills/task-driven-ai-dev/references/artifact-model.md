# Artifact Model

Use these files to keep the harness durable across sessions and across tools.

## `architecture.md`

Purpose:
- Describe the system, not the latest implementation trivia.
- Capture constraints, integrations, data model, key flows, and acceptance boundaries.

Minimum sections:
- Project overview
- Goals and non-goals
- Stack and external dependencies
- Core flows
- Data model or state model
- API or interface surface
- Risks and validation requirements

Start from `assets/templates/architecture.md`.

## `task.json`

Purpose:
- Hold the executable backlog.
- Give future agents a machine-readable source of truth.

Recommended fields per task:
- `id`
- `title`
- `description`
- `steps`
- `priority`
- `dependencies`
- `passes`
- `blocked`
- `blocked_reason`
- `validation_notes`

Rules:
- Keep task granularity small enough for one guarded iteration.
- Never delete historical tasks to hide mistakes.
- Use dependencies only for real sequencing constraints.

Start from `assets/templates/task.json`.

## `progress.txt`

Purpose:
- Preserve a truthful timeline of work, testing, and blocks.

Each entry should answer:
- What changed?
- How was it tested?
- What should future agents know?

Keep block entries explicit and searchable.

Start from `assets/templates/progress.txt`.

## `project-config.json`

Purpose:
- Externalize repo-specific commands and paths so the harness is reusable.

Capture:
- app root
- bootstrap commands
- dev-server commands
- validation commands
- browser-test triggers
- artifact file paths

Start from `assets/templates/project-config.json`.

## Adapter files

Tool-specific memory files such as `CLAUDE.md`, `AGENTS.md`, or Cursor rules are adapters. Generate them from the canonical artifact set instead of making them the only source of truth.
