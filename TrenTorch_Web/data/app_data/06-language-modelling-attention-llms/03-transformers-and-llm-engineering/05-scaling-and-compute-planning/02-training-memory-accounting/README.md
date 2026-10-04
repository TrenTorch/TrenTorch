---
name: lm-training-memory-accounting
title: Training Memory & ZeRO
tags: [training, memory, zero]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Training a model needs far more memory than the weights alone. With mixed-precision Adam the usual per-parameter bill is 2 bytes for the bf16 weights, 2 bytes for the bf16 gradients and 12 bytes of optimizer state (a 4-byte fp32 master copy of the weights plus two 4-byte moment estimates): **16 bytes per parameter**. A 7-billion-parameter model therefore needs over 100 GB before counting a single activation. **ZeRO** removes the redundancy of data parallelism by sharding these three components across `n` GPUs: stage 1 shards the optimizer state, stage 2 also shards the gradients and stage 3 also shards the weights.

### From theory to code

Implement `bytes_per_param` and `training_memory_gib`.

### Constraints

- The three components are weights `2`, gradients `2` and optimizer state `12` bytes per parameter.
- `bytes_per_param(zero_stage, n_gpus)` returns the bytes per parameter held by **one** GPU. Stage `0` shards nothing. Stage `1` divides the optimizer state by `n_gpus`. Stage `2` also divides the gradients. Stage `3` also divides the weights. Any other stage raises `ValueError`.
- `training_memory_gib(n_params, zero_stage, n_gpus)` is `n_params * bytes_per_param(...) / 2**30`, ignoring activations.
- `n_gpus >= 1`.

### Hints

<details>
<summary>Hint 1</summary>

Start from `[2, 2, 12]` and divide the components that the stage shards.

</details>

<details>
<summary>Hint 2</summary>

A GiB is `2**30` bytes.

</details>

## Theory

### The simple version

A team of data-parallel GPUs is like several students who each photocopy the entire textbook. ZeRO has each student keep one chapter and borrow the others when needed, so the class owns one copy between them.

### The formula

$$
b(\text{stage}, n) = \underbrace{\tfrac{2}{n^{[s \ge 3]}}}_{\text{weights}} + \underbrace{\tfrac{2}{n^{[s \ge 2]}}}_{\text{grads}} + \underbrace{\tfrac{12}{n^{[s \ge 1]}}}_{\text{optimizer}}
$$

where $[s \ge k]$ is $1$ if true and $0$ otherwise. At stage 3 the bill approaches $16/n$ bytes per parameter.

### How this is done in practice

DeepSpeed ZeRO and PyTorch FSDP implement these stages. Sharding trades memory for extra communication (gathering weights for each layer), and activation memory is cut separately with gradient checkpointing.

## Explanation

The function is a small table lookup with divisions. Placing the stages in a single function makes the tests compare them directly: each stage uses strictly less memory than the previous one for `n > 1`.
