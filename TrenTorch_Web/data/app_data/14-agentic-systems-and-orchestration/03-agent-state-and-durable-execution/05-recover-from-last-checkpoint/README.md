---
name: agentic-state-recover-from-checkpoint
title: Recover an Interrupted Agent From Its Last Checkpoint
tags: [agentic-systems, agent-state, durable-execution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Checkpointing (see *Checkpoint an Agent So It Can Resume After Failure*) is only useful if recovery actually finds the *right* checkpoint — not the first one saved, not the last one saved regardless of when the crash happened, but the most recent one that existed *before* the crash. Pick the wrong one and recovery either redoes more work than necessary (picking an earlier checkpoint than it needed to) or, worse, tries to resume from a state that didn't actually exist yet at the time of the crash.

### From theory to code

You're given every checkpoint ever saved, as `(step_number, state_snapshot)` pairs — not necessarily given in step order — and the `crash_step` the run was on when it failed. Implement `find_recovery_checkpoint(checkpoints, crash_step)`. Return the `state_snapshot` of the checkpoint with the **largest** `step_number` that is still `<= crash_step` — the most recent valid recovery point at or before the crash. Return `None` if no checkpoint qualifies (every saved checkpoint happens to be after `crash_step`).

### Constraints

- 0 to 500 checkpoints; step numbers within the log may repeat or arrive in any order.

### Hints

<details>
<summary>Hint 1</summary>

Track a running "best so far" (the checkpoint with the largest qualifying step number seen), updated as you scan — you don't need to sort the checkpoints first, since a single linear scan tracking the best qualifying candidate is both simpler and doesn't depend on input order at all.

</details>

<details>
<summary>Hint 2</summary>

A checkpoint saved exactly *at* `crash_step` still counts — the boundary is inclusive (`<=`), not strict (`<`). The run was still valid at that exact step before the crash happened.

</details>

## Theory

### The simple version

Scan every checkpoint once, keeping track of the best (highest step number) one seen so far that's still at or before the crash point. Any checkpoint after the crash point is irrelevant — it describes a state the run never actually reached before failing.

### Why "largest qualifying step," not "most recently saved checkpoint" in list order

Checkpoints might not arrive in step order at all (a distributed system's checkpoints can be logged out of sequence), so "the last one in the list" and "the one with the highest step number" aren't necessarily the same thing. What actually matters for correctness is *how far the run had progressed* when that checkpoint was taken, not what position it happens to occupy in whatever list you were handed.

### How this shows up in real systems

This exact "find the latest valid recovery point" search is the core of crash recovery in any durable execution system — a workflow engine restarting a job, a database recovering from its write-ahead log, or an agent runtime resuming after a crash are all doing the same fundamental thing: scan available recovery points, discard anything that couldn't have existed yet at the failure point, and recover from whichever qualifying point represents the most progress.

## Explanation

The function tracks two pieces of running state as it scans `checkpoints` once: `best_step` (initialized below any real step number) and `best_snapshot`. For each checkpoint, it's only considered a candidate if `step <= crash_step` (the inclusive boundary that lets a checkpoint saved exactly at the crash step still qualify); among candidates, only one strictly greater than the current `best_step` replaces it, which is what naturally produces "the largest qualifying step number" without needing to sort the input first — order of iteration doesn't affect the final result, since every candidate is compared directly against the best one found so far regardless of where it appears in the list. If no checkpoint ever satisfies the `step <= crash_step` condition, `best_snapshot` remains at its initial `None` and is returned as-is.
