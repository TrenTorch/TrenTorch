---
name: inf-batch-dynamic-request-batching
title: 'Implement Dynamic (Static-Window) Request Batching'
tags: [inference, batching, scheduling, serving]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Processing one request at a time under-utilizes an accelerator (GPUs are efficient at large matmuls, not many tiny ones); waiting to accumulate a large batch before running anything hurts latency for early-arriving requests. Implement a dynamic (static-window) batching policy: incoming requests are grouped into a batch either once `max_batch_size` requests have arrived, or once `max_wait_time` has elapsed since the oldest currently-waiting request arrived — whichever happens first.

### From theory to code

```
close_time = min(t0 + max_wait_time, time at which the batch reaches max_batch_size)
```

where `t0` is the oldest unbatched request's arrival time.

### Constraints

- Process arrivals in chronological order (already sorted by arrival time).
- A batch closes (and a new one starts) the instant it reaches `max_batch_size`.
- If a batch hasn't reached `max_batch_size`, it closes at `batch_start_time + max_wait_time` even if a new request would otherwise have joined later.
- Return the list of batches (each a list of request ids) and each batch's close time.

### Hints

<details>
<summary>Hint: Check timeout before admitting</summary>

Track the current open batch's start time (the first request's arrival in that batch). Every subsequent request either joins if the batch isn't full yet and hasn't timed out, or starts a new batch. A request arriving exactly at the timeout boundary should be treated as arriving after closure (`>=`), to avoid an off-by-one ambiguity.

</details>

## Theory

### The simple version

An elevator that either leaves the moment it's full, or leaves after a maximum wait even half-empty rather than making the first person who got on wait forever for it to fill up.

### The formula

```
close_time = min(batch_start_time + max_wait_time, moment batch reaches max_batch_size)
```

This static-window scheme is the simplest form of request batching; `[04-simulate-continuous-batching]` and `[05-chunked-prefill-scheduling]` build on it to avoid the head-of-line blocking a static window can still cause when one request in a batch runs far longer than the others.

### How PyTorch actually implements this

This is scheduling/queueing logic operating on plain Python values (timestamps and ids) — there is no tensor computation to port to PyTorch.

## Explanation

Checking the timeout condition BEFORE admitting each new arrival (rather than only at fixed clock ticks) correctly closes a stale batch exactly at `current_start + max_wait_time` even when the next arrival comes in much later, while the `len(current_batch) == max_batch_size` check immediately after admission closes a batch the instant it's full — together the two checks implement "whichever trigger fires first" without needing a real-time event loop. This event-driven (rather than tick-based) simulation style is what `[04-simulate-continuous-batching]` also uses, just checked at every decode step instead of at every arrival.
