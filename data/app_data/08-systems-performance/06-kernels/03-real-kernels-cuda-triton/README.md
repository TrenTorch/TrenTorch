---
name: systems-perf-real-kernels-cuda-triton
title: 'Note: Real Kernels Are Written in CUDA/Triton, Not NumPy, What Changes and Why'
tags: [mlops, kernels]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every "kernel" this track has discussed so far (`01`/`02`) was reasoned about abstractly, as a black box that reads memory, computes, and writes memory. A real GPU kernel isn't one sequential black box at all — it's launched as a _grid_ of many thousands of independent threads running (conceptually) all at once, and mapping "one operation per array element" onto "one thread per array element" is the very first thing any real CUDA or Triton kernel has to work out, correctly, before it computes anything.

### From theory to code

Implement `compute_grid_size(n_elements, threads_per_block)`, `global_thread_index(block_idx, thread_idx, threads_per_block)`, and `simulate_kernel_launch(n_elements, threads_per_block)` — the exact indexing scheme real CUDA and Triton kernels use to map a grid of threads onto an array, including the bounds-checking a non-exact-multiple array size requires.

### Constraints

- `compute_grid_size` rounds _up_ (ceiling division) — a partially-full last block still needs to be launched in full.
- `global_thread_index(block_idx, thread_idx, threads_per_block)` returns `block_idx * threads_per_block + thread_idx`.
- `simulate_kernel_launch` marks a position covered only when its `global_thread_index` is strictly less than `n_elements` — some threads in the last block will compute an index _past_ the real array and must be skipped, exactly as a real kernel's bounds check does.
- Every valid position from `0` to `n_elements - 1` ends up covered exactly once.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`-(-n_elements // threads_per_block)` is a standard integer trick for ceiling division without importing `math.ceil` — negate, floor-divide, negate again.

</details>

<details>
<summary>Hint 2</summary>

When `n_elements` isn't an exact multiple of `threads_per_block`, the _last_ block still launches with a full `threads_per_block` threads — some of them compute a `global_thread_index >= n_elements` and must do nothing, which is exactly what the `if gid < n_elements` check inside `simulate_kernel_launch` is for.

</details>

## Theory

### The simple version

Think of a CUDA/Triton kernel launch like assigning workers to seats in a stadium, organized into sections (blocks) of a fixed number of seats each (threads per block). If the exact number of workers needed doesn't perfectly fill whole sections, you still have to open one more, partially-empty section — and the workers sitting in the empty seats of that last section need to know to simply do nothing, rather than trying to process a worker's task that doesn't actually exist.

### The formula

```text
compute_grid_size(n, block_size)        = ceil(n / block_size)
global_thread_index(bid, tid, block_size) = bid * block_size + tid
simulate_kernel_launch(n, block_size):
    for bid in range(compute_grid_size(n, block_size)):
        for tid in range(block_size):
            gid = global_thread_index(bid, tid, block_size)
            if gid < n:
                mark position gid as covered
```

### How PyTorch actually implements this

Context only, untested by your submission: this exact `blockIdx.x * blockDim.x + threadIdx.x` formula, paired with a `gid < n` bounds check, is the literal first pattern taught in NVIDIA's own CUDA C++ Programming Guide and in Triton's own kernel tutorials — every real elementwise CUDA or Triton kernel a framework like PyTorch dispatches to under the hood starts with exactly this indexing scheme, before doing any actual math. This is the layer of reasoning NumPy hides completely: `x + y` in NumPy never asks "which thread handles which element," because NumPy has no concept of threads at all — it's the price a real GPU kernel pays for the parallelism NumPy simply doesn't offer.

## Explanation

`compute_grid_size` uses ceiling division so that even a `1`-element remainder still gets an entire extra block launched to cover it — a real kernel launch configuration is always specified with whole blocks, never a fractional one.

`global_thread_index` is the single formula every thread in a real launch uses to compute exactly one flat array position from its own `(block_idx, thread_idx)` pair — `block_idx * threads_per_block` skips past every earlier block's full complement of threads, and `+ thread_idx` lands on this specific thread's own position within its own block.

`simulate_kernel_launch` loops over every `(block_idx, thread_idx)` pair the launch configuration implies, computes each one's `global_thread_index`, and only marks a position covered when that index is a genuinely valid array position (`< n_elements`) — this is the exact bounds check a real kernel performs to safely ignore the "extra" threads in a partially-full final block, without which those threads would read or write past the end of the actual array.
