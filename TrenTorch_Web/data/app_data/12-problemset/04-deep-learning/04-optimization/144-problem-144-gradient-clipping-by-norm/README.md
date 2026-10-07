---
name: problem-144-gradient-clipping-by-norm
title: 'Gradient Clipping by Norm'
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'gradient stability'
hint: 'scale = min(1, clip / global_norm); multiply every gradient by it'
tools: [NumPy]
---

## Statement

Clip a list of gradient arrays by their **global** norm. Compute $\|g\|=\sqrt{\sum_k\|g_k\|^2}$ over all arrays together; if it exceeds `clip`, multiply every array by `clip / ||g||`, otherwise leave them unchanged.

Implement `solve(grads,clip)`.

**Returns.** Return a list of NumPy arrays with the same shapes as the inputs. If the global norm is $0$ the arrays are returned unchanged.

### Examples

**Example 1**

Input:

```python
solve([[3.0, 4.0]], 1.0)
```

Output:

```text
[[0.6, 0.8]]
```

**Example 2**

Input:

```python
solve([[3.0], [4.0]], 10.0)
```

Output:

```text
[[3.0], [4.0]]
```

**Example 3**

Input:

```python
solve([[3.0], [4.0]], 2.5)
```

Output:

```text
[[1.5], [2.0]]
```

## Theory

### The simple version

Occasionally a single bad batch produces an enormous gradient, and one step along it can wreck the weights. Gradient clipping caps the size of the update while keeping its direction, which is essential for training RNNs and transformers stably.

### The formula

$$g\leftarrow g\cdot\min\!\Big(1,\frac{c}{\|g\|_2}\Big)$$

## Explanation

Using one _global_ norm over all parameter tensors rescales them all by the same factor, so the relative direction between layers is preserved (clipping each tensor separately would distort it). In the first example the norm is $5$, so everything is scaled by $1/5$. In the third the global norm is also $5$ and the scale is $0.5$.
