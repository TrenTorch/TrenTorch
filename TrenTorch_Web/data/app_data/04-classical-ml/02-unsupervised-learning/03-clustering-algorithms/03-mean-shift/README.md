---
name: unsupervised-mean-shift
title: 'Mean shift clustering'
tags: [classical-ml, unsupervised, clustering, density]
difficulty: Advanced
---

## Statement

### The problem, from first principles

k-means needs you to choose k. Mean shift does not. Think of each point as a climber on a density landscape: it repeatedly moves to the weighted average of nearby points, which climbs toward a peak. Points that climb to the same peak belong to the same cluster, and the number of peaks is discovered from the data, controlled by one bandwidth parameter.

Implement `mean_shift(X, bandwidth, max_iter=300, tol=1e-6)`, which returns integer cluster labels with the Gaussian kernel.

1. Start each point at its own position.
2. Move each point to the kernel-weighted mean of all data, with weights w = exp(−‖m − x‖² / (2h²)). Repeat until the largest move is below `tol` or `max_iter` is reached.
3. Merge converged positions: walk through them in order, and assign each to an existing mode if it lies within `bandwidth / 2` of that mode, otherwise start a new mode.
4. Labels are the mode indices, numbered from 0 in order of creation.

### Constraints

- `bandwidth` must be positive, otherwise raise `ValueError`.
- Do not modify `X`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the full point-to-point squared distance matrix each iteration, then take `weights @ X / weights.sum(axis=1, keepdims=True)`.

</details>

<details>
<summary>Hint 2</summary>

For the merge step, keep a list of mode centers and compare each converged point against that list.

</details>

## Theory

### The simple version

Every point walks uphill toward the nearest peak of point density. Peaks closer than about the bandwidth count as one cluster. A bigger bandwidth smooths the landscape and merges peaks.

### The formula

$$
m \leftarrow \frac{\sum_j x_j \, e^{-\lVert m - x_j\rVert^2 / (2h^2)}}{\sum_j e^{-\lVert m - x_j\rVert^2 / (2h^2)}}
$$

## Explanation

`mean_shift` iterates the kernel-weighted mean for all points at once using matrix operations, stops when the shift is negligible, and merges converged points into modes within half a bandwidth. Using `bandwidth / 2` for merging stops tiny numerical differences in the converged positions from creating extra clusters.
