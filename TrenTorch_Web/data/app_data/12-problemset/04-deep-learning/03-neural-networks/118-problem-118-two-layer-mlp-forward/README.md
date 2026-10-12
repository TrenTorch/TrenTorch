---
name: problem-118-two-layer-mlp-forward
title: 'Two-Layer MLP Forward'
tags: [problemset, dl-core, forward-pass]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'forward pass'
hint: 'z1 = X@W1 + b1; h = max(z1, 0); Y = h@W2 + b2; cache (z1, h)'
tools: [NumPy]
---

## Statement

Compute the forward pass of a two-layer network with a ReLU hidden layer: $z_1=XW_1+b_1$, $h=\max(z_1,0)$, $Y=hW_2+b_2$. Also return the intermediate values needed for backpropagation.

Implement `solve(X, W1, b1, W2, b2)`.

**Returns.** Return a tuple `(Y, (z1, h))` where the second element is the cache of pre-activation and hidden activation.

### Examples

**Example 1**

Input:

```python
solve([[1, 2]], [[1, 0], [0, 1]], [-1, 1], [[2], [3]], [0])
```

Output:

```text
([[9]], ([[0, 3]], [[0, 3]]))
```

**Example 2**

Input:

```python
solve([[2]], [[1]], [-1], [[4]], [1])
```

Output:

```text
([[5]], ([[1]], [[1]]))
```

## Theory

### The simple version

A two-layer network applies a linear map, a non-linearity, and another linear map. Without the ReLU in the middle the two linear maps would collapse into one, so the non-linearity is what lets the network represent curved decision boundaries.

### The formulas

$$z_1=XW_1+b_1,\qquad h=\max(z_1,0),\qquad Y=hW_2+b_2$$

### Why it matters

- Two layers with a ReLU between them can represent non-linear functions.
- The cache saves what the backward pass will need.

### How it works

1. $z_1=XW_1+b_1$.
2. $h=\max(z_1,0)$.
3. $Y=hW_2+b_2$.

### Worked example

$X=(1,2)$, $W_1=I$, $b_1=(-1,1)$ give $z_1=(0,3)$, so $h=(0,3)$. Then $Y=0\cdot2+3\cdot3+0=9$: ([[9]], ([[0, 3]], [[0, 3]])).

## Explanation

The cache stores $z_1$ (needed to know which units were active) and $h$ (needed for the gradient of $W_2$), so the backward pass does not have to recompute them. In the first example $z_1=(0,3)$, $h=(0,3)$ and $Y=0\cdot2+3\cdot3=9$.
