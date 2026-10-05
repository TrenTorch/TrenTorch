---
name: agentic-state-pause-resume-run
title: Pause an Agent Run and Resume It Later
tags: [agentic-systems, agent-state, durable-execution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Pausing an agent run — for a human to review progress, or just because the system needs to shut down for a deploy — only works if resuming can trust the saved progress actually matches what's about to run. If the plan changed between pause and resume (a config update, a code deploy that altered step ordering), blindly continuing from "step 3" onward could skip steps that no longer match what was actually completed, or worse, silently redo something already done differently.

### From theory to code

You're given `full_plan` (the run's full, fixed plan, as seen by the resuming session) and `completed_steps` (what the paused session recorded as already done, in order). Implement `compute_remaining_steps(full_plan, completed_steps)`. Resuming is only safe if `completed_steps` is exactly a **prefix** of `full_plan` — the plan hasn't changed underneath the paused run. If it is, return the remaining steps (everything after the completed prefix). If `completed_steps` diverges from `full_plan` anywhere, return the literal string `"STATE_MISMATCH"` instead of guessing.

### Constraints

- 0 to 200 steps in either list; step names aren't necessarily unique within a plan.

### Hints

<details>
<summary>Hint 1</summary>

`full_plan[:len(completed_steps)] == completed_steps` is the entire validity check — it directly compares "the first N steps of the current plan" against "everything the paused run says it already did," in one list-equality comparison.

</details>

<details>
<summary>Hint 2</summary>

`completed_steps` longer than `full_plan` is also a mismatch, not a special case to handle separately — slicing `full_plan[:len(completed_steps)]` when `completed_steps` is longer just returns the whole (shorter) `full_plan`, which then correctly fails to equal the longer `completed_steps` list.

</details>

## Theory

### The simple version

Before continuing a paused run, check that everything it claims to have already finished still lines up, in the same order, with the start of the current plan. If it does, hand back whatever's left. If it doesn't, don't guess how to reconcile the difference — refuse and say so.

### Why prefix equality, not just "same length" or "same set of steps"

A resume that silently tolerates a _reordered_ or _partially different_ set of completed steps risks either skipping a step that's now actually required, or re-running a step whose position moved. Exact prefix equality is the one check that guarantees "everything the paused run did is still exactly where the current plan expects it" — nothing weaker actually guarantees that continuing from this exact point is safe.

### How this shows up in real systems

This is the same validation any durable-workflow or job-resumption system has to do before trusting a checkpoint: don't just resume blindly because a checkpoint exists — verify the checkpoint's recorded progress is still consistent with the current definition of the work before continuing from it. A checkpoint that doesn't validate is a sign something changed out from under the paused run, and the safe response is to stop and flag it, not to improvise a merge.

## Explanation

The validity check is a single list-slice comparison: `full_plan[:len(completed_steps)] != completed_steps` — slicing `full_plan` down to the same length as `completed_steps` and comparing directly catches every way the two could diverge: a different step at some position, a shorter `full_plan` than `completed_steps` (the slice comes back shorter than `completed_steps`, so they can't be equal), or `completed_steps` being out of order relative to `full_plan`. When the check passes, `full_plan[len(completed_steps):]` is exactly "everything after the validated completed prefix," computed with the same length used in the validation, so the two operations stay consistent with each other by construction. When it fails, the function returns `"STATE_MISMATCH"` immediately rather than attempting any kind of partial or best-effort continuation.
