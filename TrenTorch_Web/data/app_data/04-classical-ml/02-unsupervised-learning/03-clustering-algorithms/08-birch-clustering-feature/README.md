---
name: unsupervised-birch-clustering-feature
title: 'BIRCH clustering features'
tags: [classical-ml, unsupervised, clustering, streaming]
difficulty: Advanced
---

## Statement

### Summarize points before clustering

BIRCH compresses a large dataset into small summaries called clustering features. A clustering feature (CF) for a subcluster holds the count N, the linear sum LS, and the sum of squared norms SS. Those three numbers give the centroid and radius without storing the points.

Implement `birch_subclusters(X, threshold)`. Return `(labels, centroids)`.

1. Process rows in order. Keep a list of CFs, starting empty.
2. For each point, find the existing CF with the nearest centroid.
3. Compute the radius the CF would have if the point were added: R = sqrt(SS / N − ||LS / N||²), using the merged values.
4. If that radius is at most `threshold`, add the point to that CF. Otherwise start a new CF with this point.
5. Labels are the CF indices in creation order. Centroids are LS / N for each CF.

### Constraints

- `threshold` must be nonnegative, otherwise raise `ValueError`.
- Every returned subcluster has radius at most `threshold` (up to a floating point tolerance of 1e-9).
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

Store each CF as its N, its LS vector, and its SS scalar in three parallel lists.

</details>

<details>
<summary>Hint 2</summary>

Clamp the radius inside the square root at zero, since rounding can make it slightly negative.

</details>

## Theory

Radius is the root-mean-square distance from the members to their centroid. Because the CF keeps SS and LS, merging two CFs is just adding their components, which is what makes BIRCH fast on streams.

## Explanation

The solution keeps one CF per subcluster. Each new point is compared against the nearest centroid only, which keeps the work linear in the number of subclusters. The radius check uses the merged CF so the threshold is honest about what is stored.
