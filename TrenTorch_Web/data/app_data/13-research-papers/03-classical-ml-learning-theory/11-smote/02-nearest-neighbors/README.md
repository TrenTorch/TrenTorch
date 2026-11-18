---
name: research-smote-nearest
title: 'SMOTE: Finding Nearest Neighbors'
tags: [research-papers, classical-ml, imbalance, smote]
difficulty: Beginner
---

## Statement

### The problem, from first principles

SMOTE needs the nearest minority neighbors of each sample. The paper uses Euclidean distance, and the neighbors are chosen from the minority class only.

### From theory to code

Implement `nearest_neighbors(X, x, k)`, returning the indices of the k closest rows, nearest first.

### Constraints

- Distances are Euclidean.

### Hints

<details>
<summary>Hint 1</summary>

Compute the distance from `x` to every row, then sort the indices by distance and keep the first k.

</details>

## Theory

### The simple version

The closest points are the most plausible partners for interpolation, so restricting to nearby neighbors keeps synthetic samples realistic.

### The formula

$$\mathcal{N}_k(x) = \{\,j : d(x, x_j) \text{ is among the } k \text{ smallest}\,\}$$

### How NumPy/PyTorch actually implements this

`sklearn.neighbors.NearestNeighbors` returns the same neighbors, with a faster index structure.

## Explanation

A full sort is simple and correct for small data. Large datasets use approximate nearest-neighbor indexes instead.
