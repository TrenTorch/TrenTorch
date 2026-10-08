---
name: research-gpipe-micro-batch-size
title: 'GPipe: Micro-batch Size'
tags: [research-papers, systems, parallelism, pipeline]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Micro-batching splits the global batch so the pipeline can overlap work. Each micro-batch is smaller, and the number of them sets how full the pipeline gets.

### From theory to code

Implement `micro_batch_size(batch, micro)`, the size of each micro-batch.

### Constraints

- Use integer division.

### Hints

<details>
<summary>Hint 1</summary>

Floor-divide the batch by the number of micro-batches.

</details>

## Theory

### The simple version

Smaller micro-batches fit in memory and keep more stages busy, at the cost of less work per kernel launch.

### The formula

$$b_\mu = \left\lfloor\frac{B}{M}\right\rfloor$$

### How NumPy/PyTorch actually implements this

GPipe-style trainers split each batch with this division before scheduling the micro-batches.

## Explanation

The gradient accumulated over micro-batches equals the full-batch gradient when the batch divides evenly.
