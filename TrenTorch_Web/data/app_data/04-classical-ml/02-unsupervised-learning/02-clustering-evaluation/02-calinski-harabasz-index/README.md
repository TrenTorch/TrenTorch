---
name: unsupervised-clustering-calinski-harabasz
title: 'Calinski-Harabasz index'
tags: [classical-ml, unsupervised, clustering, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A good clustering has tight clusters that sit far from one another. The Calinski-Harabasz index (also called the variance ratio criterion) makes that precise: it compares between-cluster dispersion with within-cluster dispersion, each scaled by its degrees of freedom. Higher means a better-defined partition.

Implement `calinski_harabasz_index(X, labels)`.

- B = Σ_k n_k ‖c_k − c‖², where c_k are cluster centroids and c is the overall mean.
- W = Σ_k Σ_{x in cluster k} ‖x − c_k‖².
- Return (B / (k − 1)) / (W / (n − k)).

### Constraints

- Fewer than two clusters, or as many clusters as points, raises `ValueError`.
- If W is zero, return `inf`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the overall mean once, then each cluster's centroid and size with a boolean mask.

</details>

<details>
<summary>Hint 2</summary>

Squared distances are cheaper to sum than distances here. `np.sum((A - B) ** 2)` works on the whole cluster at once.

</details>

## Theory

### The simple version

Compare how far apart the cluster centers are, weighted by size, with how far points spread around their own centers. A large ratio means distinct groups.

### The formula

$$
\text{CH} = \frac{B / (k-1)}{W / (n-k)}
$$

## Explanation

`calinski_harabasz_index` computes the between-cluster and within-cluster sums of squares in one pass over the clusters. Dividing each by its degrees of freedom makes the index comparable across different numbers of points and clusters.
