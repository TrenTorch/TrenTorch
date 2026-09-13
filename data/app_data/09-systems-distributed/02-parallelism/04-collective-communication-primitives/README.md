---
name: systems-distributed-collective-communication-primitives
title: 'All-Reduce, All-Gather and Reduce-Scatter: The Collectives Distributed Training Is Built From'
tags: [mlops, neural-networks, distributed-training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-data-parallelism-gradient-averaging`'s `average_gradients` and `03-dataparallel-vs-distributeddataparallel`'s "ring all-reduce" were both mentioned by name without ever pinning down what an all-reduce actually _does_, or how it relates to the other collective operations (all-gather, reduce-scatter) that show up constantly in distributed-training documentation. This question implements all three directly, as the exact, general-purpose building blocks the rest of this track's questions are quietly built from.

### From theory to code

Implement `all_reduce_sum`, `all_gather`, and `reduce_scatter_sum` — three of the fundamental collective communication operations every distributed deep learning framework (NCCL, MPI, `torch.distributed`) provides.

### Constraints

- `all_reduce_sum(worker_arrays)`: every worker holds a same-shape array; returns a list where **every** worker gets the elementwise sum of all of them.
- `all_gather(worker_shards)`: every worker holds a (possibly different-sized) shard; returns a list where **every** worker gets the full concatenation of all shards, in the original order.
- `reduce_scatter_sum(worker_arrays)`: every worker holds a same-shape array; returns a list where **each** worker gets only its own chunk of the elementwise sum (the memory-efficient half of all-reduce).
- Concatenating `reduce_scatter_sum`'s output must reconstruct `all_reduce_sum`'s (single, shared) result exactly.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

All three operations start from the exact same first step: `total = sum(worker_arrays)`. All-reduce hands that whole `total` back to everyone; reduce-scatter splits it up first and hands each worker only its own piece.

</details>

<details>
<summary>Hint 2</summary>

`all_gather` is conceptually unrelated to summing at all — it's for when every worker holds a genuinely _different_ piece of data (like an embedding-table shard) and needs to see everyone else's piece too. `np.concatenate` plus copying that result into every worker's slot is the whole implementation.

</details>

## Theory

### The simple version

Imagine three people, each holding one page of a report. All-reduce is like everyone shouting their page's number out loud and every person writing down the SUM of all three numbers. All-gather is like everyone photocopying the FULL report (all three pages, stapled in order) for themselves. Reduce-scatter is like everyone shouting their numbers, summing them up once, then tearing that summed answer into three pieces and each person keeping only their own piece — useful when the combined answer is too big for any one person to hold in full.

### The formula

```text
all_reduce_sum(arrays)     -> [sum(arrays)] * len(arrays)                       -- everyone gets the FULL sum
all_gather(shards)         -> [concat(shards)] * len(shards)                    -- everyone gets the FULL concatenation
reduce_scatter_sum(arrays) -> split(sum(arrays), len(arrays))                   -- everyone gets ONE CHUNK of the sum

concat(reduce_scatter_sum(arrays)) == all_reduce_sum(arrays)[0]                 -- they reconstruct each other
```

Real GPU clusters never actually do the naive "everyone sends everything to everyone" approach implied by `sum(...)`/`concatenate(...)` — they use bandwidth-optimal ring or tree algorithms that pass partial results around a logical ring of GPUs, achieving the exact same final result as this exercise's simulated versions while moving far less data per link.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.distributed.all_reduce`, `torch.distributed.all_gather`, and `torch.distributed.reduce_scatter` are the real, NCCL-backed collectives with exactly these semantics — `DistributedDataParallel` (`03-dataparallel-vs-distributeddataparallel`) calls `all_reduce` internally to average gradients across replicas, and ZeRO-style optimizers (`05-zero-optimizer-state-sharding`) use `reduce_scatter` specifically because it never requires any single GPU to hold the full combined result in memory.

## Explanation

`all_reduce_sum` sums every worker's array elementwise, then hands that identical, full result back to each entry in the returned list — matching exactly how a real all-reduce leaves every rank holding the same, fully-combined value.

`all_gather` concatenates every worker's (possibly differently-sized) shard along axis 0, in the order the shards were given, and likewise hands that identical, full concatenation back to every worker.

`reduce_scatter_sum` does the same summing step as `all_reduce_sum`, but instead of broadcasting the whole sum back to everyone, it splits the sum into as many chunks as there are workers and hands each worker only its own chunk — this exercise's `tests.py` confirms concatenating those chunks back together exactly reconstructs what `all_reduce_sum` would have returned, the precise algebraic relationship (`reduce` + `scatter` = one collective, `all_gather`-ing the pieces back = the other) that gives reduce-scatter its name.
