# Workflow Contract

Use this protocol when the repo is managed as an AI delivery loop.

## Required artifacts

- `architecture.md`: system overview, constraints, integration boundaries, and acceptance criteria.
- `task.json`: backlog source of truth.
- `progress.txt`: dated execution log with evidence.
- `project-config.json`: repo-specific command map and artifact paths.

If one is missing, create it from the templates before claiming the harness exists.

## Single-iteration protocol

1. Rebuild context.
Read architecture, task state, recent progress, and recent commits.

2. Select exactly one task.
Prefer the first task that is not passed, not blocked, and has satisfied dependencies.

3. Verify prerequisites.
Confirm the environment, secrets, accounts, or external services required to test the task.

4. Implement.
Keep the write scope aligned with the selected task.

5. Validate.
Run the repo's required commands. Add browser validation when the task changes user-facing flows, routing, forms, or long-running async UX.

6. Update artifacts.
Mark the task passed only after validation succeeds. Write a progress entry with changes, tests, and notes.

7. Stop.
Do not silently continue into the next task.

## Git Protocol

After marking a task complete, commit the changes:

1. Stage all files related to the task:
   - Output files (documents, code)
   - Updated artifacts (task.json, progress.txt)

2. Commit with descriptive message:
   - Format: `[Task #{id}] {title}` or `[Docs] {description}`
   - Include summary of changes in commit body

3. Example:
   ```
   git add docs/analysis/01_core_module.md task.json progress.txt
   git commit -m "[Task #1] 分析 Core 模块架构"
   ```

4. Push to remote (if configured and user approves).

## Definition of done

A task is done only when all of the following are true:

- The task scope is implemented.
- Validation evidence exists.
- `task.json` reflects the new state.
- `progress.txt` explains what changed and how it was tested.
- No known unresolved blocker remains inside the claimed task scope.
- Changes are committed to git.

## Blocked protocol

If the task cannot be safely validated:

- Do not mark it passed.
- Do not commit a fake completion.
- Record the block in `progress.txt`.
- Be explicit about what a human must provide or change.
- Stop after the block is documented.

## Bugfix lane

If the planned backlog is complete but testing finds defects:

- Add explicit bugfix tasks, or
- record bugfix work as a clearly separate phase with its own validation notes.

Do not blur "backlog complete" and "post-completion repairs" into the same claim.
