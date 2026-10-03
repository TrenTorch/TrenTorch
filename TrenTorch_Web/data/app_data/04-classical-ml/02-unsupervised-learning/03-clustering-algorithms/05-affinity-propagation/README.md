---
name: unsupervised-affinity-propagation
title: 'Affinity propagation'
tags: [classical-ml, unsupervised, clustering, message-passing]
difficulty: Advanced
---

## Statement

### Clusters chosen by message passing

Affinity propagation does not ask for a number of clusters. Every point starts as a candidate exemplar, and points exchange two messages until a set of exemplars emerges. Each point then joins the exemplar it is most similar to.

Implement `affinity_propagation(X, preference=None, damping=0.5, max_iter=200)`. Use similarity S(i, k) = negative squared Euclidean distance. Put `preference` on the diagonal of S, or use the median of the off-diagonal similarities when it is `None`.

For each iteration:

1. Responsibility: R(i, k) = S(i, k) − max over k' ≠ k of (A(i, k') + S(i, k')).
2. Availability: for i ≠ k, A(i, k) = min(0, R(k, k) + Σ over i' ∉ {i, k} of max(0, R(i', k))). The diagonal A(k, k) = Σ over i' ≠ k of max(0, R(i', k)).
3. Damp both messages: new = damping · old + (1 − damping) · computed.

Points with A(k, k) + R(k, k) > 0 are exemplars. Label the exemplars 0, 1, 2 in index order. Each exemplar gets its own label, and every other point gets the label of its most similar exemplar.

### Constraints

- `damping` must satisfy 0.5 ≤ damping < 1, otherwise raise `ValueError`.
- A single point returns `[0]`.
- If no exemplar appears, use the index with the largest A(k, k) + R(k, k) as the only exemplar.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

Build S once with broadcasting, then fill its diagonal with the preference using `np.fill_diagonal`.

</details>

<details>
<summary>Hint 2</summary>

For each row, the max over k' ≠ k can be found from the top two values of A + S in that row.

</details>

## Theory

Messages measure how strongly each point wants another point as its exemplar (responsibility) and how available that exemplar is to the point (availability). The preference controls how many exemplars appear: a higher value on the diagonal makes more points exemplars.

## Explanation

The solution computes the full similarity matrix, runs damped message passing, reads exemplars from the diagonal of A + R, and assigns each point to its most similar exemplar. Exemplars are forced onto their own label so a point that is an exemplar always belongs to itself.
