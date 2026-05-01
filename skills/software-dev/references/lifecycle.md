# Lifecycle Reference

Load this file when entering or revising a lifecycle phase.

## Phase 1: Problem Definition

**Output:** `docs/problem-definition.md` plus initialized Git repository or explicit manual
version-control note, `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`, `WORKFLOW.md`,
`docs/version-history.md`, and `docs/lessons-learned.md`.

Interview the user to understand what they need. Use their language, focus on the problem,
and ask at most 3-5 focused questions. If the initial request has enough detail, draft the
problem definition directly and ask for confirmation.

At project start, load `references/version-control.md`. Check whether the directory is in
Git. If not, ask whether to initialize Git before creating project files. Record the choice
in `PROJECT.md`.

```markdown
# Problem Definition

## Problem Statement
[Clear, jargon-free description]

## Target Users / Scenario
[Who has this problem or what situation triggers it]

## Success Criteria
[Concrete, testable definition of done]

## Constraints
[Time, technology, budget, or other limits]

## Out of Scope
[What this project will not address]
```

## Phase 2: Requirements Analysis

**Output:** `docs/requirements.md`

Transform the problem into specific, testable requirements. Separate must-haves from
nice-to-haves.

```markdown
# Requirements

## Functional Requirements
- FR-001: [What the system must do]

## Non-Functional Requirements
- NFR-001: [Performance, usability, reliability, etc.]

## Constraints
[Technical or resource constraints]

## Priority
### Must-Have (MVP)
[Minimum useful scope]

### Nice-to-Have
[Useful but not required]
```

## Phase 3: Planning

**Output:** `docs/plan.md`

Choose lifecycle model, tools, milestones, risks, iteration plan, and version strategy.
Prefer short iterative cycles for small/demo projects. Include Git branch, commit, tagging,
and rollback expectations in the version strategy.

```markdown
# Development Plan

## Lifecycle Model
[Choice and rationale]

## Technology Stack
- Language:
- Framework:
- Database / Storage:
- Key Libraries:

## Milestones
1. [Milestone] — [what it demonstrates]

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## Iteration Plan
### Iteration 1: [Name]
- Scope:
- Goal:

## Version Strategy
- Initial version:
- Release cadence:
- Version bump rule:
- Git branch/commit policy:
- Tagging policy:
- Rollback approach:
```

## Phase 4: Architecture

**Output:** `docs/architecture.md`

Design major building blocks, boundaries, data flow, storage, security considerations, and
key design decisions.

```markdown
# Architecture

## System Overview
[One-paragraph structure]

## Components
### [Component Name]
- Responsibility:
- Exposes:
- Depends on:

## Data Flow
[Text description or simple diagram]

## Data Storage
[Schema, file structure, or storage approach]

## Security Considerations
[Input validation, auth, data protection]

## Key Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
```

## Phase 5: Detailed Design

**Output:** `docs/design.md`

Define modules, key functions/classes, data structures, contracts, algorithms, error
handling, coding conventions, and state management.

```markdown
# Detailed Design

## Module: [Name]
- Purpose:
- Key functions/classes:
- Data structures:
- Error handling:
- Dependencies:

## API Contracts
[Function signatures, data formats, protocols]

## Coding Conventions
- Naming style:
- Error handling pattern:
- Logging approach:

## State Management
[How state is tracked and updated]
```

## Phase 6: Coding & Debugging

**Output:** Source code in project-standard directories after the documentation gate passes.

Process:

1. Re-read `docs/design.md` and relevant requirements.
2. Read `AGENTS.md`/`WORKFLOW.md` when present and pass the Documentation Gate.
3. Run `git status --short` and identify existing user changes.
4. If intended implementation differs from docs, update docs first.
5. Commit approved documentation checkpoints when Git is enabled.
6. Set up project structure and dependencies.
7. Implement modules in dependency order.
8. Smoke test each module before moving on.
9. Wire modules together and verify the happy path.
10. Fix integration issues before polishing edge cases.
11. Update `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`, and `WORKFLOW.md` if paths, commands,
    gates, or workflows changed.
12. Commit coherent implementation slices after verification.

Exit gate: the app runs and the core happy path works end to end.

## Phase 7: Unit Testing

**Output:** Test files in `tests/` mirroring source structure.

Prioritize core business logic, input validation, boundary cases, and user-reachable error
paths. Aim for 1-2 tests per must-have requirement plus 3-5 edge case tests. Do not test
framework internals, trivial getters/setters, or third-party behavior.

Exit gate: all unit tests pass and must-priority behavior is covered.

## Phase 8: Integration

Wire components according to architecture, run end-to-end workflows, fix interface/data
format mismatches, and verify data flows through the full system.

Exit gate: all major workflows complete in the integrated system.

## Phase 9: System Testing

**Output:** `docs/test-results.md`

Test against Phase 2 requirements. Try bad input, missing steps, and out-of-order actions.

```markdown
# Test Results

## Summary
- Total scenarios tested:
- Passed:
- Failed:
- Known issues:

## Requirement Coverage
| Requirement | Test Scenario | Result |
|---|---|---|

## Known Issues
- [Description] — Severity: [High/Medium/Low]
```

Exit gate: all must-have requirements pass; known issues are documented and acceptable.

## Phase 10: Delivery

**Output:** updated project files, `README.md`, `docs/version-history.md`,
`docs/lessons-learned.md`, and final `CLAUDE.md`.

1. Write `README.md` with setup and usage.
2. Update version history with version, date, changes, verification, and rollback note.
3. Update lessons learned with reusable lessons.
4. Verify the project runs from a clean install.
5. Commit final code/docs and create a release tag when appropriate.
6. Finalize `PROJECT.md` with Delivered status, final version, and release commit/tag.
7. Finalize `CLAUDE.md` so future generic agents can resume.

Exit gate: project is delivered and maintainable.
