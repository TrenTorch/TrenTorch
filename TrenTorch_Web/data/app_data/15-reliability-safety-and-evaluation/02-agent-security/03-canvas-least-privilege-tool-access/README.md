---
name: agentic-security-canvas-least-privilege
title: Least-Privilege Tool Access
tags: [agentic-systems, agent-security, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Permissions are usually assigned per *task*, not per agent identity: a task that only reads data should run with read access, even if the agent executing it is technically capable of more. Assigning the maximum available permission "to be safe" is backwards -- it's the thing that makes an agent dangerous when it misbehaves.

### The task

Wire each task to the smallest permission level that lets it actually complete, and nothing above that.

## Theory

### The simple version

Least privilege, applied per task rather than per agent: summarizing a document needs to read it, nothing else. Drafting a reply needs to read the thread and send a message. Deleting stale records needs read, write, and delete. None of the three needs shell execution or an admin override, so neither should ever appear on the board.

### Why granting by task (not by role) matters

A single agent often runs many different tasks over its lifetime. If it's granted once, at its maximum needed level, and reuses that grant for every task, a task that only needed to read ends up executing with delete access it never asked for. Scoping the grant to the task, not the agent, keeps each individual action's blast radius as small as the action itself.

### How this shows up in real systems

This is why capability-scoped tokens and per-call permission checks exist instead of one long-lived, maximally-permissioned session: the cost of a compromised or confused single call stays bounded by what that call was actually allowed to do.

## Explanation

Each task connects to exactly the permission level it needs to finish -- read-only for summarizing, read+send for drafting a reply, full read/write/delete for cleanup -- and never to shell execution or an admin override, which no task on this board legitimately requires. The forbidden edges enforce the upper bound for every task: summarizing must never reach send, full, shell, or admin access; drafting must never reach full, shell, or admin; and even cleanup, despite needing the most access here, must never reach shell or admin.
