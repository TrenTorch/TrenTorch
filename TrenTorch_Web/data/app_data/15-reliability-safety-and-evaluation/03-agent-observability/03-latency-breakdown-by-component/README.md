---
name: agentic-observability-latency-breakdown
title: Break Down a Run's Latency by Component
tags: [agentic-systems, agent-observability, tracing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A slow agent run has one visible symptom -- it took too long -- but usually many possible causes: a slow retrieval step, a slow LLM call, a slow external tool. Fixing the slowest part first requires knowing which part it actually is, not guessing.

### The task

Write `latency_breakdown(events)` that takes a list of `(component, duration)` pairs and returns a dict mapping each component to the sum of its durations across the whole run.

## Theory

### The simple version

Group the run's events by which component produced them, and sum the durations within each group. The result answers "how much of this run's total time went to retrieval, versus the LLM, versus tools" directly.

### Why grouping by component (not just totaling the run)

A single total latency number tells you the run was slow; it says nothing about where to look. Grouping by component turns one undifferentiated number into a small breakdown that points straight at the biggest contributor -- the same reason a profiler reports time per function rather than one total runtime.

### How this shows up in real systems

This is the aggregation an APM (application performance monitoring) dashboard does automatically for a distributed trace: sum span durations per service or per operation name, so a slow endpoint's root cause is visible without reading every individual trace.

## Explanation

A running dict accumulates each component's total, using `.get(component, 0.0)` so a component seen for the first time starts from zero instead of requiring a separate initialization step -- a single pass over the events, grouped by key, summed as it goes.
