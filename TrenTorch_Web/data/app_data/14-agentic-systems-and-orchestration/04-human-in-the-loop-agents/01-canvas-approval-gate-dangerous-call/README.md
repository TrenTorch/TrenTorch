---
name: agentic-hitl-canvas-approval-gate
title: An Approval Gate Before a Dangerous Tool Call
tags: [agentic-systems, human-in-the-loop, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Some tool calls are cheap to get wrong — a re-runnable search, a read-only lookup. Others aren't — deleting a database table, sending a real email, transferring money. For the second kind, letting an agent execute autonomously the instant it decides to act removes the one safety check that actually matters: a human looking at the specific proposed call before it happens and either approving or blocking it.

### The task

Wire the approval gate so a dangerous call only ever executes after passing through it, never before.

## Theory

### The simple version

A dangerous call doesn't execute directly — it gets proposed, then held at a gate until a human looks at it, and only then does it either proceed to execution or get aborted. The gate sits strictly between "the agent decided to act" and "the action actually happens," with no path around it.

### Why the gate has to be between proposal and execution, not after

Approving *after* the call has already run defeats the entire purpose — the point of a gate is preventing an unwanted action, not reviewing one that already happened. The gate only provides real safety if execution is impossible without first passing through it, which is exactly why "execute immediately without asking" is a distractor here: it's not a shortcut, it's the specific failure mode this whole pattern exists to prevent.

### How this shows up in real systems

Human approval gates are the standard mitigation for any agent action with real, hard-to-reverse consequences — the gate itself can be as simple as a synchronous confirmation prompt or as involved as a full review queue, but the topology is always the same: propose, hold, then branch to execute-on-approval or abort-on-rejection, never execute-then-ask.

## Explanation

The chain runs `Start` -> `Dangerous tool call proposed` -> `Approval gate`, and only from the gate do two outcomes branch: `Execute the call` (on approval) or `Abort, do not execute` (on rejection) — both are legitimate endpoints, and which one actually happens is the human's decision, not the agent's. Neither distractor piece connects to anything, since both describe skipping the gate entirely (executing without asking, or merely logging instead of actually gating) — exactly the behavior this pattern is built to rule out.
