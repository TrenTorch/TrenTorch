---
name: production-inference-dynamic-windowed-batching
title: Dynamic Windowed Batching of Inference Requests
tags: [production-systems, inference-optimization]
difficulty: Medium
---

## Statement

### The problem, from first principles

Running requests through a model one at a time under-uses the hardware -- a GPU can often process a batch of several requests almost as fast as one. But waiting to fill a large batch before running anything trades throughput for latency: the first request in the batch sits idle until enough others arrive to justify running it.

### The task

Write `batch_requests(requests, max_batch_size, max_wait_ms)`. Group arrival-ordered `(arrival_time_ms, request_id)` pairs into batches: keep adding to the current batch as long as it isn't at `max_batch_size` and the next request arrived within `max_wait_ms` of the batch's first request; otherwise close the batch and start a new one.

## Theory

### The simple version

A batch has two ways to close: it fills up, or it's been open too long. Whichever happens first ends the batch and starts a new one with whatever request triggered the close.

### Why two limits, not just one

A size-only limit means a batch never closes during a quiet period -- the first request could wait indefinitely if traffic is low. A time-only limit means a burst of traffic never batches beyond whatever arrived in the window, even if far more requests are waiting. Combining both gives a bounded worst-case latency (never wait longer than `max_wait_ms`) and a bounded best-case batch size (never smaller than what a busy period would fill).

### How this shows up in real systems

This is the batching strategy behind real inference-serving frameworks (continuous/dynamic batching in vLLM, Triton, and similar servers): requests are grouped into a batch that closes on a size or time limit, letting the server trade a small, bounded amount of added latency for a large gain in GPU utilization.

## Explanation

The batch's start time is fixed the moment its first request opens it, and every later candidate is checked against both limits relative to that same fixed start -- once either the size cap or the wait window is exceeded, the batch closes exactly as it stands and the triggering request becomes the first member of the next one, guaranteeing every request lands in exactly one batch.
