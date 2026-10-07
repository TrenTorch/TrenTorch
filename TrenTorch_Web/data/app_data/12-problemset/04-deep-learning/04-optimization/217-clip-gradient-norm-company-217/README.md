---
name: clip-gradient-norm-company-217
title: 'clip-gradient-norm — DoorDash case'
tags: [problemset, dl-training-theory, gradient-vanishing-exploding, doordash]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'DoorDash'
hint: 'scale by max_norm / norm when the norm is larger'
tools: [NumPy]
---

## Statement

DoorDash-inspired demand model occasionally produces unusually large gradients that can destabilize a training step. You need to clip the gradient vector to a maximum norm so the optimizer receives a bounded update.

If the L2 norm of the gradient exceeds `max_norm`, rescale the gradient so its norm equals `max_norm`; otherwise return it unchanged. The direction is preserved.

Implement `solve(g,max_norm)`.

**Returns.** Return a float NumPy vector. A zero gradient is returned as is.

### Examples

**Example 1**

Input:

```python
solve([3, 4], 2)
```

Output:

```text
[1.2, 1.6]
```

**Example 2**

Input:

```python
solve([0.3, 0.4], 1.0)
```

Output:

```text
[0.3, 0.4]
```

## Theory

### The simple version

One unlucky batch can produce an enormous gradient, and a single step along it can wreck the weights. Clipping caps the size of the step while keeping its direction, which is standard practice for RNNs and Transformers.

### The formula

$$g\leftarrow g\cdot\min\!\Big(1,\frac{c}{\|g\|_2}\Big)$$

## Explanation

The vector $(3,4)$ has norm $5$; limiting it to $2$ scales it by $2/5$, giving $(1.2,1.6)$ whose norm is exactly $2$. A gradient already within the limit (second example) is untouched.
