---
name: unsupervised-spectral-clustering
title: 'Spectral clustering'
tags: [classical-ml, unsupervised, clustering, graph, spectral]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Some clusters are not blobs. Two interlocking rings, or a chain of points that curls back on itself, defeat k-means because it measures straight-line distance. Spectral clustering works on a similarity graph instead. Points that are strongly connected stay together, and the clusters appear as near-disconnected pieces of the graph. The eigenvectors of the graph Laplacian reveal those pieces, and k-means on the eigenvector embedding finishes the job.

Implement `spectral_clustering(W, k)`, where `W` is an `(n, n)` symmetric matrix of nonnegative affinities. Return integer labels of length `n`.

1. Compute degrees d_i = Σ_j W_ij and the symmetric normalized Laplacian L = I − D^(−1/2) W D^(−1/2).
2. Take the eigenvectors of the k smallest eigenvalues (columns of `np.linalg.eigh` output) as an `(n, k)` embedding.
3. Normalize each row to unit length. A zero row stays zero.
4. Cluster the rows with k-means, starting from farthest-first centers: row 0, then repeatedly the row farthest from all centers chosen so far. Run Lloyd iterations until labels stop changing, at most 100 times.

### Constraints

- `W` must be square and symmetric, otherwise raise `ValueError`.
- `1 <= k <= n`, otherwise raise `ValueError`.
- Do not modify `W`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Use `np.linalg.eigh`, which returns eigenvalues in ascending order. The first k columns are the k smallest.

</details>

<details>
<summary>Hint 2</summary>

Lloyd iterations are: assign each row to the nearest center, then recompute each center as its group mean.

</details>

## Theory

### The simple version

Turn the graph into coordinates where connected points sit close together. Groups that are only weakly linked to the rest get pulled into their own tight cluster in that space, so k-means finds them easily.

### The formula

$$
L = I - D^{-1/2} W D^{-1/2}
$$

## Explanation

`spectral_clustering` builds the normalized Laplacian, reads the k eigenvectors with the smallest eigenvalues, row-normalizes them, and runs a deterministic farthest-first k-means. Using deterministic initialization makes the same graph always produce the same labels, which is useful for tests and reproducible results.
