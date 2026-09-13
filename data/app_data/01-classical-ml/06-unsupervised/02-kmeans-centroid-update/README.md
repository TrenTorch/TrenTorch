---
name: unsupervised-kmeans-centroid-update
title: 'K-Means: centroid update'
tags: [classical-ml, unsupervised, clustering, kmeans]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-kmeans-assignment` answered "given wherever the centroids currently sit, which one is each point closest to." That answer is only ever as good as the guessed centroids it started from — if the centroids are in the wrong place, the assignment is wrong too. The fix is the obvious one: now that you know which points _think_ they belong to which centroid, move each centroid to where those points actually are.

That "move to where your assigned points actually are" step is the same centroid computation `04-nearest-centroid` did for labeled classes — average the points in a group to get the group's center — just applied to a group defined by "current assignment" instead of "true class." Alternate this with the assignment step and the two together are the whole K-Means algorithm.

### From theory to code

Implement `kmeans_update_centroids(input, assignments, centroids)`: for each cluster index, average the rows of `input` currently assigned to it, and use that average as the cluster's new centroid. The one piece of theory that isn't just "average a group" is what to do when a group is empty — that's called out separately in Constraints and Theory below.

### Constraints

- `input`: shape `(n_samples, n_features)`.
- `assignments`: shape `(n_samples,)`, integer cluster index per sample, as produced by `01-kmeans-assignment`'s `kmeans_assign`.
- `centroids`: shape `(k, n_features)`, the current centroids.
- Output: shape `(k, n_features)`.
- A cluster with zero points assigned to it keeps its old centroid unchanged — never average an empty group (`0/0` is undefined).
- The input `centroids` array must not be mutated in place; callers may still hold a reference to it.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Start from a copy of `centroids`, not the original — you're going to overwrite rows, and the caller's array shouldn't change underneath them.

</details>

<details>
<summary>Hint 2</summary>

For a given cluster index, `input[assignments == cluster]` selects exactly the rows currently assigned to it. Before you call `.mean(axis=0)` on that selection, check whether it has any rows at all.

</details>

## Theory

### The simple version

Think of it like recounting who lives in each neighborhood after redrawing the boundary lines: once you know which houses fall inside a boundary, the neighborhood's "center" is just the average location of the houses inside it. If a boundary happens to contain zero houses, there's nothing to average — you leave that boundary's center exactly where it was rather than pretending it's somewhere undefined.

### The formula

For cluster `j` with member set `S_j = { i : assignments[i] = j }`:

```
new_centroid[j] = mean(input[i] for i in S_j)   if |S_j| > 0
new_centroid[j] = centroid[j]                    if |S_j| = 0   (unchanged)
```

### How PyTorch actually implements this

There's no dedicated `torch` op for "K-Means centroid update"; the underlying computation is a grouped mean, the same shape as computing `input[mask].mean(dim=0)` per group, or equivalently what `torch_scatter.scatter_mean` (a common add-on, not in core `torch`) computes when scattering by cluster index. The empty-group guard here is specific to this algorithm, not something a generic reduction handles for you.

## Explanation

`kmeans_update_centroids` builds `new_centroids = centroids.copy()` (line 8) first, so the array being mutated is never the caller's original — `test_does_not_mutate_the_original_centroids_array` checks exactly this. It then loops `cluster` over `range(n_clusters)` (line 9), and for each one, `members = input[assignments == cluster]` (line 10) boolean-selects the rows currently assigned to that cluster. `if members.shape[0] > 0` (line 11) is the empty-cluster guard: only when at least one row was selected does `members.mean(axis=0)` (line 12) run and overwrite `new_centroids[cluster]`; otherwise that row is left exactly as it was copied from `centroids`, matching `test_empty_cluster_keeps_its_old_centroid`.
