---
name: research-zero-memory-per-gpu
title: 'ZeRO: Memory per GPU'
tags: [research-papers, systems, training, memory]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

ZeRO (Rajbhandari et al., 2020) removes the redundancy in data-parallel training. Mixed-precision Adam needs 16 bytes per parameter: fp16 weights and gradients, plus fp32 master weights, momentum and variance. ZeRO partitions those pieces across GPUs in stages.

### From theory to code

Implement `zero_memory_per_gpu(psi, N, stage)`, returning the per-GPU memory for the chosen stage.

### Constraints

- Stage 0 is ordinary data parallelism with no partitioning.

### Hints

<details>
<summary>Hint 1</summary>

Use the 2 bytes of fp16 weights and 2 of gradients plus 12 of optimizer state; each stage divides the parts it shards by N.

</details>

## Theory

### The simple version

Optimizer states are the largest share, so partitioning them first gives most of the saving. Stage 3 shards the weights too, so memory falls linearly with the number of GPUs.

### The formula

$$M_0 = 16\psi,\quad M_1 = 4\psi + \tfrac{12\psi}{N},\quad M_2 = 2\psi + \tfrac{14\psi}{N},\quad M_3 = \tfrac{16\psi}{N}$$

### How NumPy/PyTorch actually implements this

DeepSpeed's ZeRO configuration selects these stages; the memory estimator in DeepSpeed reproduces this formula.

## Explanation

The 12 bytes are the fp32 master weights, momentum and variance per parameter; the stages decide which of the four buckets is split.
