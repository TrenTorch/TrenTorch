---
name: unsupervised-dbscan
title: 'DBSCAN: density-based clustering'
tags: [classical-ml, unsupervised, clustering, dbscan]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

K-Means (`01`/`02`) and GMM (`04`/`05`) both need to be told `k`, how many clusters to look for, and both assume every point belongs to some cluster. Real data doesn't always cooperate: sometimes the right number of clusters isn't known ahead of time, and sometimes a handful of points genuinely are outliers that shouldn't be forced into any cluster at all.

### From theory to code

Implement `region_query(input, point_idx, eps)`, the indices of every point within `eps` of a given point (itself included), and `dbscan_fit(input, eps, min_samples)`, which grows clusters outward from dense regions and marks the rest as noise. Reuse `01-knn`'s `pairwise_distances`. `-1` means "noise," never a real cluster id — real cluster ids start at `0`.

### Constraints

- `region_query` returns indices where distance is `<= eps` (not strictly `<`), always including the query point itself.
- `dbscan_fit` returns one cluster id per row of `input`, or `-1` for noise.
- A point needs `>= min_samples` neighbors (including itself) to be a "core" point that can start or extend a cluster.
- A "border" point (within `eps` of a core point, but not itself core) joins that cluster without extending it further.
- Cluster ids are assigned in the order clusters are discovered, starting at `0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A point with fewer than `min_samples` neighbors doesn't necessarily stay noise forever — it might still get absorbed later as a border point of some other, later-discovered cluster. Don't treat "not enough neighbors right now" as a final decision.

</details>

<details>
<summary>Hint 2</summary>

Grow a cluster with a `seeds` list processed like a queue (append new neighbors to the end, advance an index rather than removing from the front) — but only extend the search through neighbors that are _themselves_ core points; a border point joins the cluster without growing it further.

</details>

## Theory

### The simple version

K-Means (`01`/`02`) and GMM (`04`/`05`) both need to be told `k`, how many clusters to look for, and both assume every point belongs to some cluster. DBSCAN (Density-Based Spatial Clustering of Applications with Noise) needs neither: it discovers the number of clusters from the data itself, and it can explicitly say "this point isn't part of any cluster" — genuine outliers, rather than forcing every point into its nearest cluster the way K-Means does.

### The formula

The core idea is density: a **core point** has at least `min_samples` other points within distance `eps` of it (a dense neighborhood). A cluster is built by starting from a core point and growing outward, absorbing every point reachable through a chain of core points' neighborhoods:

```text
pick an unvisited point
   -> region_query: how many points are within eps?
< min_samples  ->  mark noise (for now), move to the next point
>= min_samples ->  it's a core point, start a new cluster:
                    add every neighbor to the cluster
                    for each neighbor that is ALSO a core point, add ITS neighbors too
                    (breadth-first growth through core points)
```

A point can join a cluster without itself being a core point (a "border" point, close to a core point but not dense enough on its own to extend the cluster further), which is exactly why a point marked noise early on can still get absorbed into a cluster later, once some other point's growing cluster reaches it. Once every point has been visited, whatever's left labeled `-1` genuinely isn't close to any dense region — real noise, not a forced cluster assignment.

### How PyTorch actually implements this

Context only, untested by your submission: this is a classical clustering algorithm, not a PyTorch operation — the real-world equivalent is scikit-learn's `DBSCAN`, which this exercise's own `tests.py` verifies against directly (`test_matches_real_sklearn_dbscan_on_a_baked_dataset` bakes in cluster labels generated once, offline, from a real, fitted `sklearn.cluster.DBSCAN`).

## Explanation

`region_query` reuses `pairwise_distances` between the whole dataset and one query point, then `np.where(distances <= eps)[0]` for the indices within range — `<=`, not `<`, so a point exactly `eps` away still counts, and the query point itself is always included (its distance to itself is `0`).

`dbscan_fit` visits points in index order. An unvisited point with fewer than `min_samples` neighbors stays `-1` and the outer loop moves on — it's not yet known whether it'll later become a border point of someone else's cluster. A core point starts a new cluster and grows it with a `seeds` list processed like a queue (`while j < len(seeds): ... j += 1`, appending new neighbors onto the end rather than removing from the front, functionally a breadth-first search): every neighbor gets the current `cluster_id` if it doesn't already have one, and only neighbors that are _themselves_ core points (their own `region_query` also returns `>= min_samples`) get their neighbors appended to keep the expansion going — a border point joins the cluster but doesn't extend it further. `cluster_id` increments only after a cluster has finished growing completely.
