---
name: research-maxout-forward
title: 'Maxout Networks: The Maxout Unit'
tags: [research-papers, activation, maxout]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Maxout networks (Goodfellow et al., 2013) make the activation itself learnable: each unit outputs the maximum of several linear functions of its input. The paper shows this family can approximate any convex function and works well with dropout.

### From theory to code

Implement `maxout_forward(x, W, b, k)`, computing `out * k` linear pieces and returning the maximum over each group of `k`.

### Constraints

- `W` has `out * k` rows.
- Pieces for the same unit are adjacent.

### Hints

<details>
<summary>Hint 1</summary>

Compute all pieces with one affine map, reshape to `(N, out, k)`, then take the max over the last axis.

</details>

## Theory

### The simple version

Each output is the upper envelope of `k` lines in its input space. Varying the pieces lets the unit learn its own nonlinearity, from ReLU-like to absolute-value-like shapes.

### The formula

$$h_i(x) = \max_{j \in [1, k]} \left(z_{ij}\right), \qquad z_{ij} = W_{ij}^\top x + b_{ij}$$

### How NumPy/PyTorch actually implements this

Maxout is a `Linear` layer to `out * k` features followed by a reshape and max. Some libraries provide it directly as a module.

## Explanation

The reshape groups pieces by unit, so `max(axis=-1)` gives one value per unit. This is the whole layer; it has no separate activation function.
