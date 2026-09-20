---
name: agentic-orchestration-canvas-supervisor-delegation
title: A Supervisor Delegating Sub-Tasks to Worker Agents
tags: [agentic-systems, multi-agent, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A single agent trying to do everything — research, write code, draft prose — ends up mediocre at all three, since each of those is a genuinely different skill with a genuinely different ideal prompt and toolset. The supervisor pattern splits this up: one agent's only job is breaking incoming work into sub-tasks and delegating each to a _specialized_ worker built for exactly that kind of work, never doing the work itself.

### The task

Drag the right worker onto the canvas for each task type, then wire the supervisor to every task, and every task to the worker actually built for it.

## Theory

### The simple version

The supervisor never does the work — it only decides _who_ should. Each task type has exactly one worker that's actually specialized for it; the supervisor's whole value is routing correctly, not being good at research or code or writing itself.

### Why specialization beats one generalist agent

A worker built and prompted for exactly one kind of task can have a narrower, more reliable toolset, a more specific system prompt, and a much easier job to evaluate and improve in isolation — a research worker can be tuned purely for finding and citing sources, without that tuning ever having to compromise with "also be good at writing code." A single generalist agent has to be adequate at everything at once, which in practice usually means excellent at nothing.

### How this shows up in real systems

Supervisor/worker (also called orchestrator/sub-agent) topologies are the standard shape for any multi-agent system handling genuinely different kinds of sub-tasks — the supervisor's own prompt is deliberately kept narrow ("classify this request, delegate it"), which is both simpler to get right and easier to debug than one enormous agent trying to be everything to everyone.

## Explanation

Every task connects to the supervisor on one side (it's the supervisor that decided this task exists and needs handling) and to exactly one specialized worker on the other — never to a generic assistant, and never to another supervisor, since delegating further would just push the same decision down a level without ever getting real work done. The three task-to-worker pairings are each a direct one-to-one match on specialization: research work goes to the research worker, code work to the coder, writing work to the writer, mirroring exactly how a real supervisor's routing logic would be written.
