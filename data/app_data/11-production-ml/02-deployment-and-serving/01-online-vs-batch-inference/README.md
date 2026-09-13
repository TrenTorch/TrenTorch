---
name: production-ml-online-vs-batch-inference
title: 'Online vs. Batch Inference: Request-by-Request vs. Scheduled Bulk Scoring'
tags: [mlops]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A trained model has to serve real requests eventually — but "serving" isn't one single pattern. Some applications need a prediction the instant a request arrives (a fraud check on a live transaction); others just need millions of predictions computed sometime before tomorrow morning (scoring every customer for a weekly churn report). These two patterns trade off in a genuinely quantifiable way: fixed per-call overhead versus how long any individual request has to wait.

### From theory to code

Implement `online_inference` and `batch_inference` (the two calling patterns themselves), plus `online_total_overhead`, `batch_total_overhead`, and `worst_case_batch_wait_time`, quantifying the real tradeoff between them.

### Constraints

- `online_inference(model_fn, request)` calls the model on a batch of size 1 and returns that single result.
- `batch_inference(model_fn, requests)` calls the model once on the whole list.
- `online_total_overhead(num_requests, overhead_per_call)` returns `num_requests * overhead_per_call`.
- `batch_total_overhead(num_requests, overhead_per_call, batch_size)` returns `ceil(num_requests / batch_size) * overhead_per_call`.
- `worst_case_batch_wait_time(batch_size, per_request_arrival_interval)` returns `(batch_size - 1) * per_request_arrival_interval`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Every model call — online or batched — pays some fixed overhead regardless of how many items are in the batch (framework dispatch cost, a network round trip, a GPU kernel launch). Fewer, bigger calls means that fixed cost gets paid fewer times.

</details>

<details>
<summary>Hint 2</summary>

`worst_case_batch_wait_time` is about the FIRST request into an otherwise-empty batch: it has to sit and wait for `batch_size - 1` MORE requests to show up (each taking roughly `per_request_arrival_interval` to arrive) before the whole batch actually gets processed.

</details>

## Theory

### The simple version

Imagine a coffee shop that can either make each customer's order the moment they order it (online: fastest per-customer service, but the barista re-sets-up their whole station for every single cup), or wait until 5 orders have piled up and make all 5 drinks in one go (batch: the setup cost gets shared across 5 drinks, but the FIRST person in that group of 5 has to wait for 4 more people to show up before their coffee even starts). Neither approach is universally "better" — it depends entirely on whether customers value speed or the shop values throughput more.

### The formula

```text
online_total_overhead(n, overhead)              = n * overhead
batch_total_overhead(n, overhead, batch_size)    = ceil(n / batch_size) * overhead

worst_case_batch_wait_time(batch_size, interval) = (batch_size - 1) * interval
```

At `batch_size=1`, batching's formulas reduce to exactly the online case — batching is a strict generalization, not a fundamentally different mechanism, and this exercise's `tests.py` confirms that identity directly.

### How PyTorch actually implements this

Context only, untested by your submission: real model-serving frameworks (NVIDIA Triton Inference Server, TorchServe) implement "dynamic batching" precisely to capture batch inference's throughput benefit automatically — they hold incoming requests briefly, grouping whatever arrives within a short time window into one batch, explicitly trading a small amount of added latency (bounded by a configurable max wait time, directly analogous to `worst_case_batch_wait_time`) for substantially higher overall throughput.

## Explanation

`online_inference` and `batch_inference` are thin wrappers making the calling PATTERN explicit — this exercise's final oracle test confirms they're functionally equivalent when applied consistently (calling the model on each request individually, one at a time, produces the exact same results as calling it once on the whole list), so the choice between them is purely an operational one, not a difference in what gets computed.

`online_total_overhead` and `batch_total_overhead` quantify the fixed-cost side of the tradeoff directly — `tests.py` confirms batching strictly reduces total overhead for any batch size greater than 1, that larger batches reduce it further, and that a partially-full final batch still costs a FULL overhead charge (rounding up), a real, easy-to-overlook detail.

`worst_case_batch_wait_time` quantifies the other side of the tradeoff: the latency cost batching imposes on whichever request happens to arrive first into a batch, growing linearly with batch size — the exact number a real system's "max batch wait time" configuration knob is trying to bound.
