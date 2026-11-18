---
name: research-weight-norm-row-norms
title: 'Weight Normalization: Row Norms'
tags: [research-papers, normalization, weight-norm]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Weight normalization needs the length of each weight vector, and it has to be computed per output unit. This question isolates that step.

### From theory to code

Implement `row_norms(v)`, returning the Euclidean norm of each row of `v`.

### Constraints

- Returns an array of length `out`.

### Hints

<details>
<summary>Hint 1</summary>

Square, sum across each row (axis 1), then take the square root.

</details>

## Theory

### The simple version

Each output unit's weight vector has its own length `||v_i||`. Dividing by it is what turns `v` into a unit direction.

### The formula

$$\|\mathbf{v}_i\|_2 = \sqrt{\sum_j v_{ij}^2}$$

### How NumPy/PyTorch actually implements this

`torch.linalg.vector_norm(v, dim=1)` computes the same row norms.

## Explanation

The row sums run over the input axis, one per output unit. This matches the per-unit normalization used in `weight_norm`.
