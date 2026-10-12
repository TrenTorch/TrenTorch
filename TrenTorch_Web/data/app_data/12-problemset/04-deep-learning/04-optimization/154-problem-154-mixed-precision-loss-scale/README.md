---
name: problem-154-mixed-precision-loss-scale
title: 'Mixed Precision Loss Scale'
tags: [problemset, dl-training-theory, numerical-stability]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'numerical stability'
hint: 'loss * scale, and each gradient divided by scale'
tools: [NumPy]
---

## Statement

Apply static loss scaling for mixed-precision training. Multiply the loss by `scale`, and divide every gradient array in `scaled_grads` by the same `scale` to recover the true gradients. `scale` must be positive.

Implement `solve(loss, scaled_grads, scale)`.

**Returns.** Return `(scaled_loss, unscaled_grads)` where the second item is a list of NumPy arrays; a non-positive scale raises `ValueError`.

### Examples

**Example 1**

Input:

```python
solve(2.0, [[8.0, 4.0]], 4.0)
```

Output:

```text
(8.0, [[2.0, 1.0]])
```

**Example 2**

Input:

```python
solve(0.5, [[-6.0]], 2.0)
```

Output:

```text
(1.0, [[-3.0]])
```

## Theory

### The simple version

Half-precision (float16) numbers cannot represent very small values: tiny gradients underflow to zero and training stalls. Scaling the loss up by a big factor makes the gradients proportionally bigger and keeps them representable. Before the weight update the gradients are divided by the same factor so the update is unchanged.

### The identity

$$\nabla(s\cdot L)=s\cdot\nabla L\;\Longrightarrow\;\nabla L=\frac{\nabla(sL)}{s}$$

### Why it matters

- Half-precision (float16) numbers cannot represent very small values, so tiny gradients underflow to zero and training stalls.
- Scaling the loss up shifts the gradients into the representable range; they are scaled back before the weight update.

### How it works

1. Multiply the loss by `scale`.
2. Divide each gradient by the same `scale`.
3. A non-positive scale raises `ValueError`.

### Worked example

Loss $2$ with scale $4$ becomes $8$. The scaled gradient $(8,4)$ is divided by $4$ to give the true gradient $(2,1)$, so the result is (8.0, [[2.0, 1.0]]).

## Explanation

Scaling and unscaling cancel exactly in real arithmetic, so the only effect is moving the gradients into a safer numeric range. Dynamic loss scaling (as in PyTorch AMP) additionally adjusts `scale` when infinities appear.
