---
name: problem-151-gradient-accumulation
title: 'Gradient Accumulation'
tags: [problemset, dl-training-theory, batch-dynamics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'batch dynamics'
hint: 'np.mean of the stacked gradients over axis 0'
tools: [NumPy]
---

## Statement

Average a list of equally shaped micro-batch gradients element-wise. Gradient accumulation sums the gradients of several small batches before one optimiser step, imitating a large batch that would not fit in memory.

Implement `solve(grads)`.

**Returns.** Return a NumPy array with the common shape of the gradients. An empty list or gradients of different shapes raise `ValueError`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 3.0], [3.0, 5.0]])
```

Output:

```text
[2.0, 4.0]
```

**Example 2**

Input:

```python
solve([[2.0, -2.0], [4.0, 0.0], [6.0, 2.0]])
```

Output:

```text
[4.0, 0.0]
```

## Theory

### The simple version

A big batch gives a smoother gradient but may not fit on the GPU. Instead, run several micro-batches, add up their gradients, and update once. Averaging (rather than summing) keeps the gradient the same size as it would be for one large batch.

### The formula

$$\bar g=\frac1M\sum_{m=1}^{M}g_m$$

### Why it matters

- When a large batch does not fit in memory, you can process it in micro-batches and combine their gradients before taking one optimiser step.
- Averaging (rather than summing) keeps the update the same size as it would be for the single large batch.

### How it works

1. Check that there is at least one gradient and all have the same shape.
2. Stack them along a new first axis.
3. Average over that axis.

### Worked example

The gradients $(1,3)$ and $(3,5)$ average coordinate by coordinate: $(1+3)/2=2$ and $(3+5)/2=4$, so the result is [2.0, 4.0].

## Explanation

The arrays are stacked and averaged along the new first axis. For equal-sized micro-batches and a mean-reduced loss this equals the gradient of the full batch exactly.
