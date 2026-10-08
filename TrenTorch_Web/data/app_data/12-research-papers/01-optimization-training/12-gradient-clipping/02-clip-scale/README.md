---
name: research-clip-scale
title: 'Gradient Clipping: The Clip Scale'
tags: [research-papers, optimization, stability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The clip multiplier is the scalar that clip-by-norm applies. Separating it out makes the rule explicit: it is one when the norm is within bounds and shrinks the gradient otherwise.

### From theory to code

Implement `clip_scale(norm, threshold)`, the scalar clipping multiplier.

### Constraints

- The multiplier never exceeds one.

### Hints

<details>
<summary>Hint 1</summary>

Take the minimum of one and the threshold divided by the norm.

</details>

## Theory

### The simple version

The multiplier makes clipping a single cheap scalar, so the same value can be applied to every parameter tensor in a model.

### The formula

$$s = \min\!\left(1,\frac{\tau}{\lVert g\rVert}\right)$$

### How NumPy/PyTorch actually implements this

Clipping code computes one global norm across all tensors and applies this single scale to each of them.

## Explanation

Hand case: threshold 2 over norm 10 gives 0.2.
