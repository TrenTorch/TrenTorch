---
name: research-megatron-row-allreduce
title: 'Megatron-LM: Summing Row-parallel Partial Outputs'
tags: [research-papers, systems, parallelism, training]
difficulty: Beginner
---

## Statement

### The problem, from first principles

In a row-parallel layer each device computes a partial product over its share of the input features. Summing those partial results across devices reproduces the full output. The sum is an all-reduce collective.

### From theory to code

Implement `allreduce_sum(parts)`, summing the partial results element-wise.

### Constraints

- All parts have the same shape.

### Hints

<details>
<summary>Hint 1</summary>

Stack the partial results and sum over the device axis.

</details>

## Theory

### The simple version

The all-reduce is the communication cost of tensor parallelism. Megatron places it once per block so that the rest of the work stays local to each device.

### The formula

$$y = \sum_{i=1}^{p} x_i W_i$$

### How NumPy/PyTorch actually implements this

NCCL's all-reduce performs this sum across GPUs in the same way.

## Explanation

Each partial product is a matmul over a slice of the inner dimension, so the sum is exact.
