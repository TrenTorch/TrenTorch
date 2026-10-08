---
name: research-shampoo-accumulate
title: 'Shampoo: Accumulating Preconditioners'
tags: [research-papers, optimization, preconditioning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Shampoo (Gupta et al., 2018) preconditions a matrix gradient on both sides, using a running sum of G G^T on the left and G^T G on the right. Those sums capture the curvature along each axis.

### From theory to code

Implement `accumulate_preconditioners(L, R, G)`, adding the two gram matrices of the gradient.

### Constraints

- Return the pair (L, R).

### Hints

<details>
<summary>Hint 1</summary>

Add G times G transposed to L, and G transposed times G to R.

</details>

## Theory

### The simple version

Two-sided preconditioning uses far less memory than a full curvature matrix over all weights, yet still captures structure across both matrix axes.

### The formula

$$L \leftarrow L + GG^\top,\qquad R \leftarrow R + G^\top G$$

### How NumPy/PyTorch actually implements this

Production Shampoo recomputes the roots of L and R only every few hundred steps to save compute.

## Explanation

Hand case: G = [[1, 0]] gives G G^T = [[1]] and G^T G = [[1, 0], [0, 0]].
