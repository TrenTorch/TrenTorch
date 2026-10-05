---
name: unsupervised-clustering-davies-bouldin
title: 'Davies-Bouldin index'
tags: [classical-ml, unsupervised, clustering, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Silhouette scores each point. Sometimes you want a single number for the whole clustering that asks whether clusters are compact and far apart. The Davies-Bouldin index does that: for each cluster, find the most similar other cluster (similar means spread-to-separation ratio is high), then average those worst-case ratios. Lower is better, and 0 is the floor.

Implement `davies_bouldin_index(X, labels)`.

1. For each cluster i, compute its centroid and its scatter S_i, the mean distance from its points to the centroid.
2. For each pair i ≠ j, compute R_ij = (S_i + S_j) / d(centroid_i, centroid_j).
3. Return the mean over clusters i of max over j ≠ i of R_ij.

### Constraints

- Fewer than two distinct labels raises `ValueError`.
- Use Euclidean distance.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Use `np.unique(labels)` to loop over clusters, and compute each centroid with a boolean mask.

</details>

<details>
<summary>Hint 2</summary>

Build the full k-by-k matrix of centroid distances, then mask out the diagonal before taking the max.

</details>

## Theory

### The simple version

Each cluster is judged by its worst neighbor. A cluster that is tight and far from everything else scores low. If two clusters are spread out and close together, they pull the average up.

### The formula

$$
\text{DB} = \frac{1}{k}\sum_{i=1}^{k} \max_{j \neq i} \frac{S_i + S_j}{\lVert c_i - c_j \rVert}
$$

## Explanation

`davies_bouldin_index` computes centroids and scatters for each cluster, forms the pairwise ratio matrix from the centroid distances, and averages the worst ratio per cluster. The k-by-k matrix keeps the max over neighbors a single vectorized step.
