---
name: manifold-isomap
title: 'Isomap'
tags: [classical-ml, unsupervised, manifold, geodesic]
difficulty: Advanced
---

## Statement

### Distances along the manifold

Euclidean distance can be misleading on a curved manifold: two points on opposite ends of a rolled-up sheet look close in space even though they are far apart along the surface. Isomap measures distance along the surface instead, then embeds those geodesic distances with classical MDS.

Implement `isomap(X, n_neighbors, n_components)`. Return coordinates of shape `(n, n_components)`.

1. Build the k-nearest-neighbor graph. Connect each point to its `n_neighbors` nearest points by Euclidean distance. Make the graph symmetric, so an edge exists if either endpoint lists the other.
2. Set edge weights to the Euclidean distance between the endpoints.
3. Compute all-pairs shortest path lengths with Floyd-Warshall. These are the geodesic distances.
4. If any geodesic distance is infinite, raise `ValueError` because the graph is disconnected.
5. Run classical MDS on the geodesic distance matrix and keep `n_components` coordinates.

### Constraints

- `1 ≤ n_neighbors < n`, otherwise raise `ValueError`.
- `1 ≤ n_components ≤ n`, otherwise raise `ValueError`.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

Use a matrix of `inf` for the graph, set the diagonal to zero, then write the edge lengths in both directions.

</details>

<details>
<summary>Hint 2</summary>

Floyd-Warshall is three nested loops over k, i, j, or a vectorized update: `D = np.minimum(D, D[:, [k]] + D[[k], :])` for each k.

</details>

## Theory

For data sampled from a smooth manifold, shortest paths through a dense neighbor graph approximate arc length along the surface. Classical MDS then flattens those distances into a low-dimensional space, which unrolls the manifold when the approximation is good.

## Explanation

The solution builds the symmetric neighbor graph, runs Floyd-Warshall to get geodesics, checks connectivity, and calls the same double-centering and eigendecomposition used for classical MDS.
