---
name: production-inference-pick-model-under-budget
title: Pick the Best Model That Fits a Latency Budget
tags: [production-systems, inference-optimization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Given several candidate models with different quality and latency, the goal usually isn't "the best model" in the abstract -- it's the best model that still meets a hard latency requirement (a user-facing endpoint with a 200ms SLA, say). A model that scores higher but blows the budget isn't a real option.

### The task

Write `pick_model_under_budget(models, latency_budget_ms)`, where each model is `(name, quality_score, latency_ms)`. Return the name of the highest-quality model whose latency fits within the budget, or `None` if no model qualifies.

## Theory

### The simple version

This is a constrained argmax: first filter to the models that satisfy the hard constraint (latency within budget), then take the best by the actual objective (quality) among only that filtered set.

### Why filter first, rather than picking the global best and checking after

Picking the globally best-quality model and then checking whether it fits the budget throws away useful information the moment it doesn't -- there's no fallback path back to the next-best option without redoing the search. Filtering to the feasible set first means the argmax only ever considers models that were actually usable, so the result is correct without a second pass.

### How this shows up in real systems

This is the same shape as any constrained resource-selection problem in a production system: pick the cheapest instance type that still meets a memory requirement, the fastest algorithm that still fits a time budget, or here, the strongest model that still meets a latency SLA -- constraint first, optimization objective second.

## Explanation

Only models with `latency_ms <= latency_budget_ms` are ever considered as candidates; among those, a running best is kept using a strict `>` comparison, so the first model reaching a given quality score keeps its position over a later one that merely ties it. If no model survives the latency filter, the running best stays `None` and that's exactly what's returned.
