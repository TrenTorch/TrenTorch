---
name: inf-batch-continuous-batching
title: 'Simulate Continuous (Iteration-Level) Batching'
tags: [inference, continuous-batching, scheduling, serving]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[03-dynamic-request-batching]`'s static batching processes one whole batch to completion before forming the next — so if 7 of 8 requests finish quickly but 1 needs 500 more tokens, the other 7 slots sit idle waiting for that straggler. Simulate continuous batching (a.k.a. iteration-level scheduling, as used in vLLM/TGI): at every decode step, any request that has finished is removed from the active batch and any waiting request is admitted into the freed slot immediately.

### From theory to code

```
remaining_tokens[r] -= 1   for every active request r, at each decode step t
active = (active - finished) + admitted_from_queue,  |active| <= max_batch_size
```

### Constraints

- Requests are given as `(arrival_step, request_id, n_tokens_needed)`.
- At each step: decrement remaining tokens for every active request by 1, evict any that reach 0, then admit from the FIFO wait queue (among requests that have arrived by this step) to refill up to `max_batch_size`.
- Simulation ends when every request has been fully generated.
- Return, per request, the step at which it was admitted and the step at which it finished.

### Hints

<details>
<summary>Hint: Evict before admit, same step</summary>

Process eviction before admission WITHIN each step: a request that finishes exactly at this step frees its slot in time for a new admission at the SAME step, not the next one. Preserve arrival order for the waiting queue (FIFO) when deciding which queued request gets an opening slot first.

</details>

## Theory

### The simple version

A restaurant that seats a new party the INSTANT any table becomes free, rather than waiting until every table in the current "seating round" is empty before seating anyone new.

### The formula

```
each step: remaining[r] -= 1 for r in active
           evict r where remaining[r] == 0
           admit from queue to refill up to max_batch_size
```

This is the single biggest throughput improvement over naive static batching for LLM serving, precisely because request generation lengths vary enormously and a straggler should never block everyone else's slot.

### How PyTorch actually implements this

This is discrete-event scheduling over plain Python state (dicts/lists of integers) — there is no tensor computation to port; the same scheduler sits in front of whichever framework runs the actual per-step forward pass.

## Explanation

Running eviction (removing requests whose `remaining_tokens` just hit 0) before the next call to admission logic guarantees a freed slot is visible to admission in the very same step it opened up — exactly the iteration-level granularity that distinguishes continuous batching from static batching, where slots only reopen once the whole batch completes. This is why continuous batching's throughput advantage grows with generation-length VARIANCE across requests: if every request needed exactly the same number of tokens, static and continuous batching would perform identically (no stragglers to route around), but real workloads have generation lengths varying by 10x or more, which is exactly the gap continuous batching closes.
