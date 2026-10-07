---
name: problem-117-linear-layer-backward
title: 'Linear Layer Backward'
tags: [problemset, dl-core, backpropagation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'backpropagation'
hint: 'dX = dY @ W.T; dW = X.T @ dY; db = dY.sum(axis=0)'
tools: [NumPy]
---

## Statement

Compute the backward pass of a dense layer $Y=XW+b$. Given the layer input `X`, the upstream gradient `dY` (same shape as $Y$) and the weights `W`, return the gradients with respect to the input, the weights and the bias.

Implement `solve(X, dY, W)`.

**Returns.** Return a tuple `(dX, dW, db)` where `dX = dY @ W.T`, `dW = X.T @ dY` and `db` sums `dY` over the batch.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0]], [[1.0, -1.0]], [[1.0, 0.0], [0.0, 1.0]])
```

Output:

```text
([[1.0, -1.0]], [[1.0, -1.0], [2.0, -2.0]], [1.0, -1.0])
```

**Example 2**

Input:

```python
solve([[1.0], [2.0]], [[3.0], [4.0]], [[2.0]])
```

Output:

```text
([[6.0], [8.0]], [[11.0]], [7.0])
```

## Theory

### The simple version

Backpropagation applies the chain rule layer by layer. For a linear layer the three needed gradients are all matrix products of the things you already have: the upstream gradient tells you how much the loss cares about each output, and the layer's inputs and weights say how that blame is shared.

### The formulas

$$\frac{\partial L}{\partial X}=dY\,W^\top,\qquad \frac{\partial L}{\partial W}=X^\top dY,\qquad \frac{\partial L}{\partial b}=\sum_{\text{batch}}dY$$

## Explanation

Shapes are the easiest check: $dX$ must match $X$ ($n\times d_{in}$), $dW$ must match $W$ ($d_{in}\times d_{out}$) and $db$ must match $b$ ($d_{out}$). The bias gradient sums over the batch because the same bias was added to every row.
