---
name: agentic-state-canvas-state-machine
title: A State Machine for an Agent Instead of a Linear Loop
tags: [agentic-systems, agent-state, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A plain ReAct loop assumes the agent is always in the same "mode": think, act, observe, repeat. Real agent runs aren't that uniform — a run can be actively planning, actively executing, sitting idle waiting for a human's approval before a risky action, or having already failed or finished. Modeling these as one linear loop hides real, distinct states an agent run can be in, each with different valid next moves. A state machine makes those states and their legal transitions explicit.

### The task

Wire the six real states into the only transitions that are actually legal for this agent — every fixed node is already on the canvas; your job is connecting them correctly, and leaving the two distractor pieces unwired.

## Theory

### The simple version

An agent isn't always "running" in the same sense — it can be idle, planning what to do, actually executing, paused waiting on a human, or has already ended (successfully or not). A state machine names each of these explicitly and defines exactly which transitions between them are legal, instead of pretending the whole run is one undifferentiated loop.

### Why "waiting for approval" loops back to "executing," not "planning"

Approval is a pause in the _middle_ of already-decided work, not a reason to re-plan from scratch — once approved, execution should simply continue where it left off. Routing the approval state back to planning would throw away a decision the agent already made and force needless re-work; routing it back to executing correctly treats the human's approval as a gate on continuing, not a reason to start over.

### How this shows up in real systems

Real production agent runtimes model exactly this kind of explicit state machine — not because it's more "correct" in the abstract, but because a linear loop genuinely can't represent "paused indefinitely waiting on an external human," "resumed after a crash," or "definitely done, never runs again" as first-class states with their own rules about what can happen next. A durable execution system (see the next question in this track) is built directly on top of a state machine exactly like this one.

## Explanation

Six real states, six real transitions: `Idle` starts every run and only ever moves to `Planning`, which only ever moves to `Executing` once a plan exists. From `Executing`, three outcomes are legal — reaching `Done` on success, encountering something that needs a human's sign-off (`Waiting for Approval`), or failing outright (`Failed`) — and `Waiting for Approval` only ever resumes back into `Executing`, never anywhere else, since approval is a pause on already-decided work, not a restart. The two distractor pieces, `Retry` and `Paused`, are deliberately not real states in this machine: retrying is just re-entering `Executing` again (not a separate state), and pausing indefinitely is a different mechanism covered by a different question in this track.
