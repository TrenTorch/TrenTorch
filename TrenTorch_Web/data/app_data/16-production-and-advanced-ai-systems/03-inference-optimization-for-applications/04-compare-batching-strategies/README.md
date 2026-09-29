---
name: production-inference-compare-batching-strategies
title: Compare Individual vs. Batched Processing Cost
tags: [production-systems, inference-optimization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Batching helps because per-request overhead (loading weights into the compute path, kernel launch setup, whatever fixed cost a single call pays) doesn't scale with the number of requests inside a batch -- it's paid once per batch, not once per request. Quantifying that savings is what tells you whether batching is actually worth the added complexity for a given workload.

### The task

Write `compare_batching_strategies(num_requests, max_batch_size, per_request_ms, per_batch_overhead_ms)`. Processing individually pays the fixed overhead on every single request; batching in groups of up to `max_batch_size` pays it once per batch. Return a dict with `"individual_total_ms"`, `"batched_total_ms"`, and `"savings_ms"`.

## Theory

### The simple version

Individual cost is `num_requests * (per_request_ms + per_batch_overhead_ms)` -- every request pays both its own processing time and the fixed overhead alone. Batched cost is `num_requests * per_request_ms + num_batches * per_batch_overhead_ms` -- the per-request work is unavoidable either way, but the fixed overhead is now shared across up to `max_batch_size` requests per payment.

### Why the number of batches rounds up

A batch of `max_batch_size` requests still needs a full batch's overhead even if the last group only has one leftover request in it -- there's no such thing as half a batch's setup cost. Rounding the batch count up is what correctly reflects that any partial group still needs the same fixed overhead as a full one.

### How this shows up in real systems

This is the calculation behind a capacity-planning decision: whether the throughput or cost gain from batching is large enough to justify the added latency and complexity, given the actual overhead-to-processing-time ratio the deployment is dealing with.

## Explanation

Individual cost pays the overhead once per request; batched cost pays the per-request time regardless (since the actual work per request doesn't shrink) but pays the fixed overhead only `ceil(num_requests / max_batch_size)` times -- the number of batches needed to fit everyone, rounding up because a partial final batch still needs its own overhead payment.
