---
name: agentic-observability-build-trace
title: Build a Trace of an Agent Run
tags: [agentic-systems, agent-observability, tracing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A single agent run might call an LLM, then a tool, then the LLM again, then another tool -- and when something goes wrong (or costs too much, or takes too long), the question is always "which step, and when." A trace answers that: a timeline of every step in a run, in order, with when it started and how long it took.

### The task

Write `build_trace(events)` that takes a list of `(name, kind, duration)` events run one after another with no overlap, and returns one dict per event with its name, kind, `start_offset` (seconds since the run began), and `duration`.

## Theory

### The simple version

Walk the events in order, keeping a running clock. Each event's `start_offset` is wherever the clock currently sits; then advance the clock by that event's duration before moving to the next one.

### Why offsets, not just durations

A list of durations alone can't answer "what was happening at second 3.5 into the run" without recomputing the running sum every time someone asks. Precomputing the offset once, when the trace is built, is what makes a trace viewer (or a "show me everything between t=2 and t=5" query) a simple lookup instead of a repeated recomputation.

### How this shows up in real systems

This is the same structure behind distributed tracing spans (each span has a start time and duration relative to the trace's root) -- an agent run is just a single-threaded trace where every step happens sequentially instead of concurrently.

## Explanation

A running `start_offset` accumulator starts at zero, records itself on the current event before advancing by that event's duration, so the very first event always starts at offset zero and each later one starts exactly where the previous one ended -- a plain cumulative sum walked once, left to right.
