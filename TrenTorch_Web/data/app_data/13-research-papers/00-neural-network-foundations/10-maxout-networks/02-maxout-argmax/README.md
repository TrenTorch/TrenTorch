---
name: research-maxout-argmax
title: 'Maxout Networks: Which Piece Wins?'
tags: [research-papers, activation, maxout]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The maxout unit only sends gradient through the piece that wins. Knowing which piece wins for each input is what turns the max into a piecewise-linear function, and it determines the backward pass.

### From theory to code

Implement `maxout_argmax(x, W, b, k)`, which returns the index of the winning piece for each unit and example.

### Constraints

- Indices are in `[0, k-1]`.

### Hints

<details>
<summary>Hint 1</summary>

Use the same grouping as `maxout_forward`, but call `argmax` on the last axis instead of `max`.

</details>

## Theory

### The simple version

The winning index says which linear piece is active. In backprop, only that piece's weights receive gradient for that example.

### The formula

$$j^*(i) = \arg\max_{j} z_{ij}$$

### How NumPy/PyTorch actually implements this

Autograd does this implicitly: the gradient of `max` flows only to the argmax element.

## Explanation

The active piece selects a single affine map per unit, so the layer is locally linear in its input.
