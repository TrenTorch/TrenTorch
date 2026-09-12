---
name: inf-batch-chunked-prefill
title: 'Simulate Chunked Prefill Scheduling'
tags: [inference, chunked-prefill, scheduling, serving]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A long prompt's prefill run in one shot can take far longer than a single decode step for other concurrently running requests — those requests effectively stall until the huge prefill finishes, spiking their inter-token latency. Simulate chunked prefill scheduling: a long prompt's prefill is split into fixed-size chunks and interleaved with ongoing decode steps for other requests, instead of running the entire prefill in one uninterrupted burst.

### From theory to code

```
budget_left = token_budget - n_active_decode_requests    -- 1 token-unit per active decode request
chunk_size = min(budget_left, tokens_left_in_prefill)      -- spent on the next prefill request in FIFO order
```

### Constraints

- Requests are given as `(arrival_step, request_id, prefill_tokens)` — after finishing prefill each produces exactly `n_decode_tokens_each` output tokens (a shared constant across all requests) before completing.
- Every step: 1 token-unit budget goes to each already-decoding request; remaining budget is spent, in FIFO arrival order among prefill-phase requests, up to `chunk_size` tokens each.
- A request whose prefill finishes this step starts decoding from the NEXT step onward.
- Return, per request, the step its prefill finished and the step it fully completed.

### Hints

<details>
<summary>Hint: Reserve decode budget first, every step</summary>

Reserve exactly 1 token-unit of budget per currently active decode-phase request BEFORE touching any prefill chunk, every single step. Once a prefill request's remaining tokens hit 0, it transitions to a decode-phase request starting the NEXT step (it does not get a decode token in the same step its prefill finishes).

</details>

## Theory

### The simple version

A print shop with one printer and a fixed number of pages it can print per hour. Small, quick jobs (decode steps) always get their page printed first, every hour, without exception. Whatever printing capacity remains after those is spent chipping away at one giant print job (prefill) a little at a time, rather than blocking every small job until the giant one finishes.

### The formula

```
each step: budget = token_budget
           budget -= 1 per active decode request (always first)
           spend remaining budget on prefill chunks, FIFO order
```

This is the same core tension `[04-simulate-continuous-batching]` addresses (don't let one request's needs starve everyone else), but for prefill/decode interleaving specifically rather than for varying generation lengths.

### How PyTorch actually implements this

This is scheduler/queueing simulation over plain Python counters — no tensor math is involved; the same scheduler decides, per step, which requests' actual forward passes (implemented in NumPy or PyTorch) get how many tokens of work.

## Explanation

Deducting 1 token-unit of budget for every active decode-phase request BEFORE touching the prefill queue guarantees decode requests are never starved, matching the requirement that they always get priority; a request only moves from the prefill set into the decode set after its chunked prefill total reaches exactly 0, which — because chunks are additive and FIFO-ordered — reproduces the same total prefill token count as an unchunked prefill, just spread across more steps. This additivity is what makes chunked prefill a pure scheduling change rather than an approximation: the total compute done is identical to running the prefill in one shot, only its TIMING relative to other requests' decode steps changes.
