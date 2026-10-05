---
name: research-weight-norm-linear
title: 'Weight Normalization: A Linear Layer'
tags: [research-papers, normalization, weight-norm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A weight-normalized layer is an ordinary linear layer whose weight matrix is built from `g` and `v`. Using it as a drop-in replacement shows the reparameterization is just a change of variables.

### From theory to code

Implement `weight_norm_linear(x, v, g, b)`, which builds `W` with weight normalization and returns `x W^T + b`.

### Constraints

- Output shape is `(N, out)`.

### Hints

<details>
<summary>Hint 1</summary>

Build `W` the same way as `weight_norm`, then apply the affine map.

</details>

## Theory

### The simple version

The layer's function is fixed by `W`, but `W` is parameterized by `g` and `v`. Gradient descent on `g` and `v` acts on length and direction directly.

### The formula

$$y = x\,W^\top + b, \qquad W_i = \frac{g_i}{\|v_i\|}\, v_i$$

### How NumPy/PyTorch actually implements this

The same computation is what a `Linear` layer with weight normalization performs internally.

## Explanation

Any `x @ W.T + b` layer can be rewritten this way. The reparameterized form changes the optimization geometry, not the set of functions the layer can express.
