---
name: unsupervised-optics
title: 'OPTICS ordering'
tags: [classical-ml, unsupervised, clustering, density]
difficulty: Advanced
---

## Statement

### Density ordering instead of one radius

DBSCAN needs one radius `eps`, so clusters of different densities cannot all be found at once. OPTICS builds an ordering of the points in which nearby dense points come next to each other, and records a reachability distance for each point. Valleys in the reachability plot are clusters, and different cuts through the plot recover clusters at different densities.

Implement `optics(X, min_samples, max_eps=inf)`. Return `(ordering, reachability)`.

1. Core distance: the distance to the `min_samples`-th nearest point, counting the point itself. If it is larger than `max_eps`, the core distance is infinite.
2. Start with any unprocessed point, mark it processed, and append it to the ordering.
3. If its core distance is finite, update the seeds: for each unprocessed neighbor o within `max_eps`, set reachability(o) = min(current, max(core(p), d(p, o))).
4. Repeatedly take the unprocessed seed with the smallest reachability, append it, and expand it the same way when its core distance is finite.
5. When no seeds remain, start from the next unprocessed point.

Points that were never reached keep reachability `inf`.

### Constraints

- `1 ≤ min_samples ≤ n`, otherwise raise `ValueError`.
- Ties in the seed choice go to the lower index.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

Sort each row of the distance matrix once. The core distance is the entry at index `min_samples − 1`.

</details>

<details>
<summary>Hint 2</summary>

Use a boolean mask of unprocessed points and `np.argmin` on the reachability values of the seeds.

</details>

## Theory

Reachability of o from p is the larger of p's core distance and the distance between them. The ordering visits every point of a dense region before leaving it, so a jump in reachability marks the boundary between two regions.

## Explanation

The solution computes the full distance matrix, derives core distances from the sorted rows, and runs the seed-expansion loop. Reachability is stored by point index, so the caller can read it in any order.
