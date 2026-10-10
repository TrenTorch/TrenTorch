---
name: problem-119-two-layer-mlp-backward
title: 'Two-Layer MLP Backward'
tags: [problemset, dl-core, backpropagation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'backpropagation'
hint: 'dW2 = h.T @ dY; dz1 = (dY @ W2.T) * (z1 > 0); dW1 = X.T @ dz1; dX = dz1 @ W1.T'
tools: [NumPy]
---

## Statement

Backpropagate through the two-layer ReLU network of the previous problem. Given the input `X`, the upstream gradient `dY` of the loss with respect to the output, the weights `W1`, `W2` and the forward cache `(z1, h)`, compute the gradients of every parameter and of the input.

Implement `solve(X, dY, W1, W2, cache)`.

**Returns.** Return a tuple `(dX, dW1, db1, dW2, db2)` of NumPy arrays with the shapes of `X`, `W1`, `b1`, `W2` and `b2`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0]], [[1.0]], [[1.0, 0.0], [0.0, 1.0]], [[2.0], [3.0]], ([[0.0, 3.0]], [[0.0, 3.0]]))
```

Output:

```text
([[0.0, 3.0]], [[0.0, 3.0], [0.0, 6.0]], [0.0, 3.0], [[0.0], [3.0]], [1.0])
```

**Example 2**

Input:

```python
solve([[2.0]], [[1.0]], [[1.0]], [[4.0]], ([[1.0]], [[1.0]]))
```

Output:

```text
([[4.0]], [[8.0]], [4.0], [[1.0]], [1.0])
```

## Theory

### The simple version

Backpropagation walks the network backwards, turning "how much does the loss care about this output?" into "how much does it care about each weight and input?". The ReLU in the middle acts as a gate: units that were off during the forward pass pass back zero gradient.

### The formulas

$$dW_2=h^\top dY,\quad db_2=\sum dY,\quad dz_1=(dY\,W_2^\top)\odot\mathbb 1[z_1>0]$$

$$dW_1=X^\top dz_1,\quad db_1=\sum dz_1,\quad dX=dz_1\,W_1^\top$$

### Why it matters

- Training a network needs gradients for every parameter.
- The ReLU passes the gradient only where the unit was active.

### How it works

1. $dW_2=h^\top dY$ and $db_2=\sum dY$.
2. $dz_1=(dY\,W_2^\top)\odot\mathbb 1[z_1>0]$.
3. $dW_1=X^\top dz_1$, $db_1=\sum dz_1$, $dX=dz_1W_1^\top$.

### Worked example

$dY=1$ and $W_2=(2,3)^\top$ give $(2,3)$; the first hidden unit was off ($z_1=0$), so $dz_1=(0,3)$. Then $dW_1$ has rows $(0,3)$ and $(0,6)$, $db_1=(0,3)$, $dW_2=(0,3)^\top$ and $db_2=1$: ([[0.0, 3.0]], [[0.0, 3.0], [0.0, 6.0]], [0.0, 3.0], [[0.0], [3.0]], [1.0]).

## Explanation

The gradient is first pushed through the second linear layer (giving the gradient with respect to $h$), then masked by the ReLU derivative, then pushed through the first linear layer. In the first example the first hidden unit was off ($z_1=0$), so no gradient reaches it: `dW1` has a zero first column.
