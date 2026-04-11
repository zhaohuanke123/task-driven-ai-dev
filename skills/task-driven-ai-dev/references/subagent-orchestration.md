# Subagent Orchestration

Use orchestration to replace shell loops, not to hide them.

## Principle

One main agent owns state. Subagents handle bounded supporting roles. The main agent decides when an iteration starts and when it ends.

## Recommended roles

### Selection agent

Purpose:
- Read the backlog and recent progress.
- Propose the next ready task.
- Surface risks, missing dependencies, and likely blockers.

Good prompt shape:
- Ask for the next safe task.
- Ask for blockers and required validation.
- Do not ask it to implement.

### Worker agent

Purpose:
- Implement one bounded task or one isolated code slice.

Good prompt shape:
- Give the exact task.
- Give the allowed write scope.
- Require validation notes and changed file paths.

### Verification agent

Purpose:
- Review the result independently.
- Look for missed tests, regressions, and false completion claims.

Good prompt shape:
- Provide the task definition and resulting diff context.
- Ask whether the completion claim is defensible.

## Orchestration loop

1. Main agent rebuilds repo state.
2. Selection agent proposes the next task.
3. Main agent confirms the task and prepares the environment.
4. Worker agent implements the task if delegation is worthwhile.
5. Verification agent checks the result if the platform supports a clean pass.
6. Main agent runs final validation, updates artifacts, and stops.

## Do not emulate `for run in 1..N`

Shell loops fail because they:
- hide state transitions,
- waste runs on blocked tasks,
- cannot judge whether testing was meaningful,
- encourage fake completion when validation is weak.

If a user wants repeated progress, use repeated explicit iterations with checkpoints after each one.

## When to stay local

Keep work in the main agent when:
- the task is tiny,
- the next action is blocked on the answer,
- the code slice is too coupled to delegate cleanly.
