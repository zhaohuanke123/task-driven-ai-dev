# Lessons From History

This file captures failure modes from a real repo that used a long-running AI task loop.

## Do not trust completion without environment reality

A login task was marked complete before the environment existed and before browser validation happened. The fix was to restore the task to incomplete, document the block, wait for human setup, then re-test.

Implication:
- completion gates must include environment readiness and the right validation mode.

## `confirm all` often breaks stage transitions

Multiple regressions came from client state updating locally without refreshing server-derived stage state.

Implication:
- stage changes and other derived workflow state need an authoritative refresh path.

## Async workflows must recover after refresh

Image and video generation stayed in `processing` because polling lived only in the browser session.

Implication:
- long-running task state must be recoverable after navigation, reload, or agent restart.

## Private storage needs signed access

Media delivery broke because the app assumed public object URLs while the storage bucket was private.

Implication:
- the harness should force agents to check real storage visibility and URL semantics.

## Post-backlog bugfixes are part of the story

The task backlog reached "complete," but real testing immediately exposed more defects.

Implication:
- the workflow must treat hardening and bugfix phases as first-class work, not as embarrassing footnotes.
