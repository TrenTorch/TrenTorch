---
name: semi-supervised-seeded-kmeans
title: 'Seeded k-means with fixed seed points'
tags: [classical-ml, semi-supervised, clustering, k-means, seeds]
difficulty: Intermediate
---

## Statement

### Cluster with a few labeled seeds that never move

Seeded k-means (Basu, Banerjee and Mooney, 2002) starts each cluster from the mean of its labeled seeds. During the iterations, seeded points keep their label, and unlabeled points are assigned to their nearest centroid.

Implement `seeded_kmeans(X, seeds, k, iters=100)`.

- `X` is `(N, d)`. `seeds` is `(N,)` with class indices `0..k-1` for seeded points and `-1` for unlabeled points.
- Initialize each centroid as the mean of its seeded points.
- Repeat: assign each unlabeled point to its nearest centroid (seeded points keep their label), then recompute each centroid as the mean of its assigned points. Stop when no label changes or after `iters` rounds.
- Return `(labels, centroids)`. `labels` is an integer array of length `N`, and `centroids` is `(k, d)`.

### Constraints

- Every class `0..k-1` must have at least one seed. Otherwise raise `ValueError`.
- A seed value outside `-1..k-1` raises `ValueError`.
- Shapes must be consistent. Otherwise raise `ValueError`.
- `k >= 1` and `iters >= 1`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Keep a boolean mask of seeded points and overwrite the assignments for those points after each nearest-centroid step.

</details>

## Theory

Seeds turn an unsupervised objective into a constrained one. The k-means objective still minimizes within-cluster squared distance, but the seeded points act as anchors that fix which cluster is which. Because seeds fix labels rather than just initial centroids, a bad seed can drag its whole cluster to the wrong place, so seed quality matters more than seed count.

### Where this shows up in production

Seeded clustering is used when a team has a handful of known examples per category and wants the rest of a catalogue or log to be grouped around them, for example grouping customer support tickets around a few example issue types. The labels produced are often reviewed in bulk, and the seeds double as a regression test: if a new data drop moves a seed away from its cluster, the pipeline should flag it.

### Using it to make decisions

Use seeded k-means when clusters are roughly spherical, you know the number of classes, and you can supply at least a few trustworthy seeds per class. Choose seeds that are typical, not borderline. Compare the result with plain k-means on the same data and check whether the seeded clusters match the seed labels for held-out labeled points. If they do not, the clusters probably do not match your classes.

### Pros and cons

**Pros:** cheap, easy to explain, and the seeds give the clusters their names, which makes results usable without a relabeling step.

**Cons:** inherits all k-means assumptions (spherical, similar-sized clusters), is sensitive to bad seeds, and converges to local optima.

## Explanation

The solution computes initial centroids from seed means, then alternates a masked assignment step and a mean update. Re-applying the seed labels after each assignment is the only place where seeds differ from standard k-means, and it guarantees that seeded points are never moved.
