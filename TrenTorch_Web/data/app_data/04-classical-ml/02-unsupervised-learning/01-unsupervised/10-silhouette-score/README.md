---
name: unsupervised-silhouette-score
title: Silhouette score
tags: [classical-ml, clustering, performance-measure]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Clustering has no labels to score against, so quality must be judged from the data itself: are points close to their own cluster and far from the others? The silhouette score summarises that for each point and averages it.

### From theory to code

Implement `silhouette_score(X, labels)` using Euclidean distance.

### Constraints

- `X` has shape `(n_samples, n_features)`; `labels` is a length-`n_samples` integer cluster assignment.
- For a point, `a` is its mean distance to the *other* points in its own cluster, and `b` is the smallest mean distance to the points of any *other* cluster.
- A point alone in its cluster has silhouette `0`. If `max(a, b) == 0`, its silhouette is `0`.
- Return `0.0` when there are fewer than two clusters. Return the mean silhouette as a Python `float`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Build the full pairwise distance matrix once with broadcasting.

</details>

<details><summary>Hint 2</summary>

Then loop over points: mask the same-cluster entries for `a`, and take a minimum of per-cluster means for `b`.

</details>

## Theory

### The simple version

A silhouette near +1 means a point sits snugly inside its cluster and far from neighbours. Near 0 it is on a boundary. Negative means it is probably in the wrong cluster.

### The formula

$$s(i) = \frac{b(i) - a(i)}{\max\{a(i),\, b(i)\}}, \qquad \text{score} = \frac{1}{n}\sum_i s(i)$$

### How libraries implement this

`sklearn.metrics.silhouette_score` computes the same average; it does not need ground-truth labels.

## Explanation

The `a` term excludes the point itself, so it divides by cluster size minus one. Returning 0 for singletons follows the standard convention rather than leaving the value undefined.
