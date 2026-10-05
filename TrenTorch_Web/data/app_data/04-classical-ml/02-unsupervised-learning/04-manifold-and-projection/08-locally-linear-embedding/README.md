---
name: lle-weights-and-embedding
title: 'Locally linear embedding'
tags: [classical-ml, manifold-learning, lle, dimensionality-reduction, eigendecomposition]
difficulty: Advanced
---

## Statement

### Reconstruct each point from its neighbours, then find a low-dimensional layout that keeps the same weights

Locally linear embedding (LLE) assumes each point lies close to a linear patch of a smooth manifold. Each point is reconstructed from its `k` nearest neighbours with weights that sum to 1. A low-dimensional embedding is then found that keeps those same weights.

Implement two functions.

- `lle_weights(X, k, reg=1e-3)`: `X` is `n` by `d`. For each point `i`, take its `k` nearest neighbours (excluding itself, ties to the lower index). Let `Z` be the neighbours minus `x_i`, and `G = Z Z^T`. Solve `(G + eps I) w = 1`, where `eps = reg * trace(G)`, or `eps = reg` when the trace is zero. Normalise `w` to sum to 1 and store it in row `i` at the neighbour columns. Return the `n` by `n` weight matrix `W`.
- `lle_embedding(W, dim)`: let `M = (I - W)^T (I - W)`. Return the eigenvectors of `M` for the second through `(dim + 1)`-th smallest eigenvalues, as an `n` by `dim` array. Skip the first eigenvector, which is constant.

### Constraints

- `X` must be 2-D, and `1 <= k < n`. Otherwise raise `ValueError`.
- `W` must be square, and `1 <= dim < n`. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

On a line of points, interior points have one neighbour on each side, so their weights are exactly one half each.

</details>

## Theory

LLE has two steps that share one idea. The reconstruction weights describe the local geometry of the data, and they are invariant to rotation, translation and uniform scaling. The embedding step looks for coordinates that are reconstructed by the same weights, which reduces to the bottom eigenvectors of a sparse matrix. The constant eigenvector is removed so the embedding is centred.

### Where this shows up in production

LLE is used in exploratory analysis of embeddings and sensor data, where a team wants a two-dimensional picture of a curved manifold without the parameters of t-SNE. It also appears as a preprocessing step before a supervised model when the data is believed to lie on a smooth low-dimensional surface, such as pose or lighting variation in images.

### Using it to make decisions

Use LLE when the data is roughly on a smooth manifold and the neighbourhood graph is connected. Check the neighbourhood size first: too small a `k` splits the graph and the embedding breaks into pieces, too large a `k` flattens curvature. For large datasets, prefer a sparse eigensolver or a method such as UMAP for speed. LLE does not provide an out-of-sample mapping, so if new points arrive you need a separate projection step.

### Pros and cons

**Pros:** the weight step is closed form per point, the method keeps local linear structure, and the embedding comes from one eigenproblem with no learning rate.

**Cons:** it is sensitive to `k` and to noise, it can collapse when the neighbourhood graph is disconnected or sparse, and global distances in the embedding can be badly distorted. The dense eigendecomposition scales cubically with `n`. There is no native way to embed new points.

## Explanation

The weight step solves a small regularized linear system for each point, and the regularization keeps the solve stable when neighbours are nearly collinear or duplicated. The embedding step forms `M` from the weight matrix and uses a symmetric eigendecomposition. Dropping the first eigenvector removes the constant direction that would otherwise dominate.
