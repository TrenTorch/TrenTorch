---
name: research-goyal-worker-count
title: 'Large Minibatch SGD: Workers per Batch'
tags: [research-papers, optimization, large-batch, distributed]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Large-batch training spreads a minibatch over many workers, each handling a slice. The number of workers needed depends on the global batch and how many examples fit on each worker.

### From theory to code

Implement `workers_for_batch(batch, per_worker)`, the number of workers needed to cover the batch.

### Constraints

- Round up so the whole batch is covered.

### Hints

<details>
<summary>Hint 1</summary>

Divide the batch by the per-worker count and take the ceiling.

</details>

## Theory

### The simple version

The worker count is what makes the large batch practical. Adding workers lets the global batch grow without each device exceeding its memory.

### The formula

$$W = \left\lceil\frac{B}{b_{\text{worker}}}\right\rceil$$

### How NumPy/PyTorch actually implements this

Data-parallel launchers compute this count to split the global batch across devices.

## Explanation

Hand case: 8192 over 256 gives 32 workers.
