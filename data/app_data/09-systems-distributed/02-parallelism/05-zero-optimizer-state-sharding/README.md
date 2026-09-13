---
name: systems-distributed-zero-optimizer-state-sharding
title: 'Note: FSDP / ZeRO, Sharding Optimizer State and Parameters Across GPUs'
tags: [mlops, neural-networks, distributed-training]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-data-parallelism-gradient-averaging`'s DDP-style data parallelism has a hidden cost this question makes explicit: every single GPU keeps a _full, redundant copy_ of the model's parameters, gradients, AND optimizer state (for Adam, that's fp32 copies of the parameters, momentum, and variance — far bigger than the parameters themselves). ZeRO (Zero Redundancy Optimizer) asks a simple question: if every GPU needs the FULL model to do a forward pass, but only needs its OWN SHARE of the optimizer's bookkeeping, why replicate the bookkeeping at all?

### From theory to code

Implement `per_gpu_memory_bytes(num_params, num_gpus, zero_stage)`, following the ZeRO paper's exact mixed-precision-Adam memory model for stages 0 (no sharding) through 3 (shard everything), and `memory_reduction_factor`, quantifying the savings against stage 0.

### Constraints

- Using bytes-per-parameter units: fp16 params = 2, fp16 gradients = 2, fp32 Adam optimizer state = 12 (fp32 param copy + momentum + variance, 4 bytes each).
- `zero_stage=0`: `(2 + 2 + 12) * num_params` — full replication, no sharding at all (16Ψ bytes, the ZeRO paper's baseline figure).
- `zero_stage=1` (P_os): shard only the optimizer state: `(2 + 2) * num_params + 12 * num_params / num_gpus`.
- `zero_stage=2` (P_os+g): also shard gradients: `2 * num_params + (2 + 12) * num_params / num_gpus`.
- `zero_stage=3` (P_os+g+p): shard everything: `(2 + 2 + 12) * num_params / num_gpus`.
- Any other `zero_stage` raises `ValueError`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Only the pieces that get "sharded" at a given stage get divided by `num_gpus`; everything not yet sharded at that stage stays fully replicated (multiplied by `num_params` alone, no division).

</details>

<details>
<summary>Hint 2</summary>

Sanity check: at `num_gpus=1`, every stage's formula collapses back to exactly `zero_stage=0`'s — sharding across one GPU is sharding across nobody.

</details>

## Theory

### The simple version

Imagine a team of 8 people who each need the full text of a shared document to do their work (so everyone keeps their own full copy of the _document_), but only ONE person needs to remember the full revision history for any given paragraph — instead of all 8 people memorizing the ENTIRE revision history redundantly, they split it up: each person memorizes only 1/8th of it, and consults their teammate whenever they need a piece they don't personally hold. ZeRO applies exactly this idea to a GPU's optimizer state, then (at higher stages) to gradients, then even to the parameters themselves.

### The formula

```text
K = 12    (fp32 Adam optimizer state: param copy + momentum + variance, 4 bytes each)

per_gpu_memory_bytes(Ψ, N, stage=0) = (2 + 2 + K) * Ψ            = 16Ψ    -- fully replicated everywhere
per_gpu_memory_bytes(Ψ, N, stage=1) = (2 + 2) * Ψ + K*Ψ/N                -- optimizer state sharded
per_gpu_memory_bytes(Ψ, N, stage=2) = 2*Ψ + (2 + K)*Ψ/N                  -- + gradients sharded
per_gpu_memory_bytes(Ψ, N, stage=3) = (2 + 2 + K) * Ψ / N         = 16Ψ/N -- everything sharded

memory_reduction_factor(Ψ, N, stage) = per_gpu_memory_bytes(Ψ, N, 0) / per_gpu_memory_bytes(Ψ, N, stage)
```

Since optimizer state (`K=12`) dwarfs the parameters and gradients (`2` each) for Adam, stage 1 alone already captures most of the possible savings — going from stage 1 to stage 3 buys progressively less, which is exactly the real-world tradeoff behind choosing a ZeRO stage: higher stages shard more (more memory saved) but also require more frequent communication to reconstruct the full parameters/gradients when they're actually needed for compute.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact memory model from "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models" (Rajbhandari et al., 2019), the paper behind Microsoft's DeepSpeed. PyTorch's own `FullyShardedDataParallel` (FSDP) implements the equivalent of ZeRO stage 3 natively — sharding parameters, gradients, and optimizer state across all GPUs, and temporarily all-gathering a layer's full parameters right before it's needed for compute, then immediately freeing them again.

## Explanation

`per_gpu_memory_bytes` directly encodes each stage's formula from the ZeRO paper: stage 0 keeps every component (`2 + 2 + 12`) fully multiplied by `num_params` with no division at all; each higher stage moves one more component from "fully replicated" to "divided by `num_gpus`", strictly decreasing total per-GPU memory — `tests.py` confirms `stage0 > stage1 > stage2 > stage3` holds for any `num_gpus > 1`, and that `zero_stage=3, num_gpus=1` exactly equals `zero_stage=0` (sharding across one GPU changes nothing).

`memory_reduction_factor` divides stage 0's baseline by whichever stage's memory was requested — for stage 3, `tests.py` confirms this simplifies to exactly `num_gpus`, since full sharding scales the entire `16Ψ` baseline down by that same factor.
