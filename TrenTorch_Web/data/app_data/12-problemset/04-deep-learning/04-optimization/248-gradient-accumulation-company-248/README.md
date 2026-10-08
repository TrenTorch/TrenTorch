---
name: gradient-accumulation-company-248
title: 'gradient-accumulation — Cloudflare case'
tags: [problemset, dl-training-theory, batch-size-and-training-dynamics, cloudflare]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Cloudflare'
hint: 'np.mean(grads, axis=0)'
tools: [NumPy]
---

## Statement

Cloudflare-inspired training job uses micro-batches because the full batch does not fit comfortably in memory. You need to accumulate and average gradients across the requested number of micro-batches before the optimizer step.

`grads` has one row per micro-batch (all rows have the same length). Return the element-wise average of the rows, the gradient a single large batch would have produced.

Implement `solve(grads)`.

**Returns.** Return a float NumPy vector.

`grads` has one row per micro-batch (all rows have the same length). Return the element-wise average of the rows, the gradient a single large batch would have produced.

Implement `solve(grads)`.

**Returns.** Return a float NumPy vector.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 0], [-1, 1]])
```

Output:

```text
[1.0, 1.0]
```

**Example 2**

Input:

```python
solve([[2.0, 4.0]])
```

Output:

```text
[2.0, 4.0]
```

## Theory

### The simple version

When a batch is too big for memory, you can process it in several micro-batches, add up their gradients, and take one optimiser step. Averaging (rather than summing) makes the result equal to the gradient of the full batch's mean loss, so the learning rate does not need to change.

### The formula

$$\bar g=\frac1M\sum_{m=1}^{M}g_m$$

### Why it matters

- When a batch does not fit in memory, the gradient of several micro-batches is accumulated before one optimiser step.
- Averaging (not summing) keeps the update the same size as for one big batch.

### How it works

1. Stack the micro-batch gradients as rows.
2. Average each column.

### Worked example

The columns are $(1,3,-1)$ and $(2,0,1)$, with sums $3$ and $3$ and means $1$ and $1$, so the averaged gradient is [1.0, 1.0].

## Explanation

The columns are averaged independently: in the first example both coordinates average to $1$. This equals the full-batch gradient only when the micro-batches have equal size and the loss is a mean.
