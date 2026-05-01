# Context Files Reference

Load this file when creating or repairing `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`,
`WORKFLOW.md`, `docs/version-history.md`, or `docs/lessons-learned.md`.

## PROJECT.md

Single source of truth for project state. Write it in Phase 1 and update it after every
phase transition.

```markdown
# Project: [Name]

## Status
- Current Phase: Phase N — [Name]
- Current Version: v0.0.0 / Unreleased / vX.Y.Z
- Last Updated: [date]

## One-Line Summary
[What this project is, in one sentence]

## Key Decisions
- Tech stack: [chosen stack]
- Lifecycle: [chosen model]
- Runtime workflow: `AGENTS.md` + `WORKFLOW.md`
- Version strategy: [semver/date-based/manual milestone]
- Version control: Git / manual fallback

## Phase Progress
- [ ] Phase 1: Problem Definition — `docs/problem-definition.md`
- [ ] Phase 2: Requirements — `docs/requirements.md`
- [ ] Phase 3: Planning — `docs/plan.md`
- [ ] Phase 4: Architecture — `docs/architecture.md`
- [ ] Phase 5: Detailed Design — `docs/design.md`
- [ ] Phase 6: Coding — source directories
- [ ] Phase 7: Unit Testing — test directories
- [ ] Phase 8: Integration
- [ ] Phase 9: System Testing — `docs/test-results.md`
- [ ] Phase 10: Delivery — `README.md`, `docs/version-history.md`, `docs/lessons-learned.md`

## Version Status
- Latest release:
- Git branch:
- Git commit/tag:
- Verification:
- Rollback note:

## Documentation Gate
- Source edits require a governing requirement/design/architecture reference.
- Bug fixes must record whether docs already define the correct behavior or need revision.
- Explicit documentation skips must be recorded with risk and follow-up docs.

## Resume Context
[2-3 sentences enough for a new conversation to continue.]
```

## CLAUDE.md

First file a generic agent reads. It prevents context loss when this skill is not explicitly
loaded.

```markdown
# CLAUDE.md

## Project State
- Status: [Phase / Delivered / Cancelled]
- Current version: [vX.Y.Z or Unreleased]
- Last updated: [date]
- Primary status file: `PROJECT.md`

## Progressive Context Loading
Read only what the task needs:

1. Read `AGENTS.md` first when present; it is the runtime navigation entry point.
2. Always read `PROJECT.md` for status, version, and resume context.
3. Read `WORKFLOW.md` before executing development work.
4. For requirements or scope questions, read `docs/problem-definition.md` and `docs/requirements.md`.
5. For architecture or design questions, read `docs/architecture.md` and `docs/design.md`.
6. For implementation work, read the governing requirement/design references before source files.
7. For verification, read `docs/test-results.md` and run the commands below.
8. For release or regression questions, read `docs/version-history.md`.
9. For recurring pitfalls, read `docs/lessons-learned.md`.
10. For Git, commits, tags, or rollback, read the skill reference `references/version-control.md`.

## Documentation Gate
Before editing source code for any bug, feature, or behavior change:

1. Identify the governing requirement/design/architecture document.
2. If the requested behavior is missing from or contradicts docs, update docs first.
3. If docs already define the correct behavior, record the implementation bug before fixing code.
4. If no governing document exists, stop and create or update one before source edits.
5. If the user explicitly confirms skipping docs, record the skip, risk, and follow-up docs in
   `PROJECT.md` or `progress.txt`.

## Durable Documents
- `PROJECT.md` — status, phase, version, resume context
- `AGENTS.md` — runtime navigation entry for future agents
- `WORKFLOW.md` — execution workflow and documentation gate
- `docs/problem-definition.md` — problem and success criteria
- `docs/requirements.md` — requirements
- `docs/plan.md` — stack, milestones, risks, version strategy
- `docs/architecture.md` — components and data flow
- `docs/design.md` — module design and contracts
- `docs/test-results.md` — verification
- `docs/version-history.md` — release and rollback history
- `docs/lessons-learned.md` — reusable lessons
- `README.md` — setup and usage

## Development Workflow
1. Pass the Documentation Gate before changing implementation.
2. Update the relevant document before changing behavior, contracts, or architecture.
3. Implement only what the document describes.
4. Run targeted tests or checks.
5. Reconcile docs, code, tests, and README if behavior changed.
6. Record version history or lessons when the change affects release state or future work.
7. Use Git commits/tags to record approved checkpoints unless version control is explicitly disabled.

## Commands
- Install:
- Test:
- Run:
- Build:
```

## AGENTS.md

Runtime navigation entry for future agents. Create it alongside `CLAUDE.md` so new
conversations load project rules before implementation details.

```markdown
# [Project Name] Agent Navigation

## Start Here
Read files in this order:

1. `AGENTS.md` — this navigation file
2. `PROJECT.md` — current phase, version, resume context, documentation gate
3. `WORKFLOW.md` — execution workflow and validation rules
4. Current task references in `task.json` and `progress.txt`
5. Governing docs in `docs/requirements.md`, `docs/design.md`, `docs/architecture.md`
6. Source files and tests only after the Documentation Gate passes

## Documentation Gate
No source edit for a bug, feature, or behavior change may start until the governing
requirement/design/architecture document is identified. If behavior changes, update docs
first. If the user confirms skipping docs, record the skip and stale-doc risk in
`PROJECT.md` or `progress.txt`.

## Runtime Files
- `WORKFLOW.md` — workflow, documentation gate, validation
- `task.json` — task list and document references
- `progress.txt` — execution history, testing evidence, skipped-doc notes
- `CLAUDE.md` — generic agent instructions
```

## WORKFLOW.md

Runtime execution guide. It may be generated from the `coding-workflow` templates, but it
must preserve this gate.

```markdown
# Development Workflow

## Documentation Gate
Before source edits:

1. Read `PROJECT.md`, `task.json`, and `progress.txt`.
2. Identify `requirement_ref` and `design_ref` for the task.
3. If a bug report is covered by existing docs, record it as an implementation bug.
4. If the behavior is new, missing, or changed, update requirements/design first.
5. If docs are skipped by explicit user confirmation, record the skip and risk.

Tasks cannot be marked complete until docs, code, and tests agree.
```

## docs/version-history.md

Use for every milestone, release, rollback, or user-visible behavior change.

```markdown
# Version History

## Unreleased
- Status:
- Planned changes:

## vX.Y.Z — [date]

### Git
- Branch:
- Commit:
- Tag:

### Changes
- [User-visible change]

### Verification
- [Command or manual scenario] — Pass/Fail

### Documentation Updated
- [Files updated]

### Rollback Note
- [How to revert or what previous version was stable]
```

## docs/lessons-learned.md

Use this file to teach future agents. Keep entries concise and actionable.

```markdown
# Lessons Learned

## [YYYY-MM-DD] [Short Title]
- Context:
- Lesson:
- Apply next time:
- Related files:
```
