---
name: systems-distributed-data-parallelism-gradient-averaging
title: 'Data Parallelism: A Toy Example Splitting a Batch Across Simulated Workers'
tags: [mlops, neural-networks, distributed-training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-memoization`'s tricks all made ONE worker's training loop cheaper. Data parallelism is the opposite strategy: instead of making one worker faster, split a single batch across MANY workers, have each compute a gradient on its own slice independently, and combine their answers back into one update — the foundational idea every larger distributed-training scheme (`04-collective-communication-primitives` through `07-ring-attention-online-softmax`) builds on.

### From theory to code

Implement `local_gradient` (the ordinary MSE gradient, computed on just one worker's shard), `split_batch_across_workers`, `average_gradients`, and `data_parallel_gradient`, which chains all three into a full toy data-parallel training step.

### Constraints

- `split_batch_across_workers` assumes the batch size divides evenly by `num_workers` (a real DDP setup requires every replica to use the same local batch size).
- `local_gradient(X_shard, y_shard, w)` computes `(2 / n_shard) * X_shard.T @ (X_shard @ w - y_shard)` — the same MSE gradient formula, applied to only that shard's rows.
- `average_gradients` is a plain elementwise mean across the list of per-worker gradients.
- `data_parallel_gradient(X, y, w, num_workers)` must equal the full-batch gradient computed directly on all of `X`/`y` at once, whenever the shards are equal-sized.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The full-batch gradient is `(2/N) * X.T @ (X@w - y)`. If you split `X`/`y` into `K` equal shards of size `N/K` and average the `K` per-shard gradients, the `K`s cancel algebraically — that's exactly why equal-sized shards make this work.

</details>

<details>
<summary>Hint 2</summary>

`split_batch_across_workers` is just `np.array_split(X, num_workers)` and `np.array_split(y, num_workers)`, zipped together shard by shard when computing local gradients.

</details>

## Theory

### The simple version

Imagine four people each grading a quarter of a stack of exams, each writing down their own quarter's average score, then averaging those four averages together — you get exactly the same number as if one person had graded and averaged the whole stack, as long as everyone graded the same number of exams. Data-parallel training is this, applied to gradients: split the batch, compute a gradient on each piece independently (in parallel, on separate GPUs), then average the results back into one gradient before taking a step.

### The formula

```text
local_gradient(X_shard, y_shard, w) = (2 / n_shard) * X_shard.T @ (X_shard @ w - y_shard)

data_parallel_gradient(X, y, w, K) = mean_{i=1..K} local_gradient(X_shard_i, y_shard_i, w)
                                    = full_batch_gradient(X, y, w)     [when all K shards are equal size]
```

The equal-shard-size requirement isn't a simplification for this exercise — it's a real constraint of `torch.nn.parallel.DistributedDataParallel`, which is exactly why every real distributed data loader (`DistributedSampler`) is built to guarantee equal per-replica batch sizes, dropping or padding the last batch if the dataset size doesn't divide evenly.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.nn.parallel.DistributedDataParallel` runs one process per GPU, each with its own full model replica and its own shard of the batch. After each replica's `.backward()` computes local gradients, DDP automatically triggers a ring all-reduce (`04-collective-communication-primitives`) that averages every replica's gradients in place, so every GPU's optimizer step sees the exact same, correctly-averaged gradient — precisely what `data_parallel_gradient` computes here in miniature.

## Explanation

`local_gradient` is unmodified MSE-gradient math, applied to whichever rows of `X`/`y` happen to live on a given worker — the function has no idea it's only seeing part of the data, which is exactly the point: each worker's computation is completely independent and needs no coordination with the others.

`split_batch_across_workers` uses `np.array_split` to divide both `X` and `y` into `num_workers` contiguous shards, keeping each worker's inputs and targets correctly paired.

`average_gradients` takes the elementwise mean of the list of per-worker gradients — the simulated stand-in for the real ring all-reduce a GPU cluster would perform.

`data_parallel_gradient` chains all three together: split the batch, compute each worker's local gradient independently, then average — and because the shards are equal-sized, this reconstructs the true full-batch gradient exactly, verified directly against it in this exercise's own `tests.py`, including a finite-difference numerical check of `local_gradient` itself.
