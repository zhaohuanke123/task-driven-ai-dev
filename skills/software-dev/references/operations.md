# Operations Reference

Load this file when handling exceptions, recovery, or phase-gate decisions.

## Exception Handling

| Scenario | Detection | Response |
|---|---|---|
| `PROJECT.md` corrupt or missing fields | File exists but unreadable or missing `Current Phase` | Ask user which phase to recover from; list completed docs as options |
| `CLAUDE.md` missing but `PROJECT.md` exists | Project state exists without generic agent entry | Create `CLAUDE.md` from existing docs and commands before continuing |
| `AGENTS.md` or `WORKFLOW.md` missing | Project has lifecycle docs but no runtime navigation or execution gate | Create them from current docs before development work continues |
| Docs and implementation disagree | Requirement/design says one thing but code/tests do another | Stop feature work, choose source of truth, then update docs before code |
| User reports a bug or broken behavior | "bug", "broken", "wrong", "fix", or behavior mismatch | Run Issue/Bug Triage: identify governing docs, update docs if behavior changes, then edit code |
| User asks to skip documentation | "just code", "no docs", "skip docs", similar | Warn once; if confirmed, record skip, risk, and follow-up docs in `PROJECT.md` or `progress.txt` |
| Version history missing | Delivered/versioned `PROJECT.md` but no `docs/version-history.md` | Create it from README, test results, and `PROJECT.md`; mark uncertain entries as inferred |
| Not a Git repository | `git rev-parse --is-inside-work-tree` fails | Ask whether to initialize Git; if declined, record manual version-control fallback in `PROJECT.md` |
| Dirty Git worktree | `git status --short` shows existing changes | Identify user changes; do not overwrite or revert unrelated changes |
| Release has no commit/tag | Delivered version exists but no Git commit/tag is recorded | Record current commit hash or create an annotated tag if appropriate |
| Lessons file missing after debugging/release | Reusable lesson exists but no `docs/lessons-learned.md` | Create it and add the lesson before closing the phase |
| Phase file missing but `PROJECT.md` says done | Required phase document absent | Rebuild from context if available; otherwise ask whether to redo that phase |
| User wants to skip phases | "directly code", "skip design", similar | Warn once with concrete risk; if confirmed, mark skipped in `PROJECT.md` |
| User abandons project | "cancel", "stop project", similar | Ask whether to mark cancelled; do not delete files |
| Scope exceeds demo project | Phase 1 reveals enterprise-scale needs | Recommend splitting scope or phased delivery |

## Revision Rules

1. Update the relevant phase file.
2. Add or extend a `## Change Log` section.
3. Trace impact through downstream docs, code, tests, README, and version history.
4. Verify `AGENTS.md`/`WORKFLOW.md` still point agents through the Documentation Gate.
5. Commit the coherent revision when Git is enabled and verification passes.
6. Update `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`, and `WORKFLOW.md` if status, paths,
   commands, gates, or workflow changed.
7. Add a lesson if the revision reveals a reusable pattern.

## Quick Phase Gate

- Phase 1: user confirms problem definition.
- Phase 2: requirements are testable and prioritized.
- Phase 3: stack, risks, milestones, and version strategy are clear.
- Phase 4: component boundaries and data flow are clear.
- Phase 5: module contracts are specific enough to code.
- Phase 6: app runs and happy path works.
- Phase 7: unit tests pass.
- Phase 8: integrated workflows complete.
- Phase 9: must-have requirements pass.
- Phase 10: README, version history, lessons, Git commit/tag, `PROJECT.md`, and `CLAUDE.md` are final.
