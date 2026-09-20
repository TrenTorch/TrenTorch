---
name: agentic-state-canvas-checkpoint-resume
title: Checkpoint an Agent So It Can Resume After Failure
tags: [agentic-systems, agent-state, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A long agent run that crashes ten steps in shouldn't have to redo all ten steps from scratch — that's slow, wasteful, and if any of those steps had side effects (sent an email, charged a card), redoing them could be actively harmful. Checkpointing solves this: after every completed step, save enough state to resume from exactly that point, so a crash only ever costs the work since the _last_ checkpoint, never the whole run.

### The task

Wire the checkpoint-and-resume cycle: every step gets checkpointed after it runs, and a crash always resumes from the last checkpoint — never a full restart, and never by pretending the crash didn't happen.

## Theory

### The simple version

Execute a step, save a checkpoint, execute the next step, save again — a steady rhythm. If a crash happens mid-step, the run doesn't restart from the very beginning; it resumes from whatever the last successfully saved checkpoint was, then continues executing from there as if the crash never interrupted anything beyond that point.

### Why resume goes back to "execute step," not back to "start"

The whole point of checkpointing is that completed work stays completed — a crash after step 7 shouldn't cost steps 1 through 6 all over again. Resuming into "execute step" (picking up wherever the last checkpoint left off) preserves that; resuming into "start" would make checkpointing pointless, since every crash would cost the entire run regardless of how much progress had already been saved.

### How this shows up in real systems

This checkpoint/resume cycle is the core mechanism behind "durable execution" frameworks for long-running agent workflows — the same idea used by workflow engines outside the AI space for exactly the same reason: expensive, long-running, side-effect-having processes need to survive a crash without either losing progress or double-executing something that already happened.

## Explanation

The cycle alternates between two real actions — execute a step, then save a checkpoint — looping back to execute the next step after each save, which is what lets an arbitrarily long run be built from the same two-node cycle repeated. A crash can happen mid-execution (wired from `Execute step`, since that's the only state where work is actually in flight and something can go wrong), and the only legal response to it is resuming from the last checkpoint back into `Execute step` — never restarting from `Start` (which would discard every already-checkpointed step) and never simply continuing as if nothing happened (the two distractor pieces), since a crash means the run's in-memory state is no longer trustworthy and only the last _saved_ checkpoint can be relied on.
