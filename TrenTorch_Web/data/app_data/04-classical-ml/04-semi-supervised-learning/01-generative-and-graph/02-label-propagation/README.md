---
name: semi-supervised-label-propagation
title: 'Label propagation on a similarity graph'
tags: [classical-ml, semi-supervised, graph, label-propagation, laplacian]
difficulty: Intermediate
---

## Statement

### Spread known labels along a similarity graph

Label propagation (Zhou et al., 2004) treats semi-supervised learning as smoothing over a graph. Each point has a seed label row `Y0` (one-hot for labeled points, zero for unlabeled ones). Labels spread along weighted edges until neighbours agree.

With `S = D^(-1/2) W D^(-1/2)`, the iteration is `F <- alpha * S F + (1 - alpha) * Y0`. Its fixed point is `F* = (1 - alpha) (I - alpha S)^(-1) Y0`.

Implement `propagate(W, Y0, alpha, iters)`. It runs `iters` iterations starting from `F = Y0` and returns `F`.

### Constraints

- `W` is a square, symmetric, nonnegative matrix with no node of zero degree. Otherwise raise `ValueError`.
- `Y0` has one row per node. Its row count must match `W`.
- `alpha` must be in the open interval `(0, 1)`. Otherwise raise `ValueError`.
- `iters` must be a nonnegative integer. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute `S` once before the loop. With `iters = 0` the output is just `Y0`.

</details>

## Theory

The graph Laplacian is the operator that penalizes label differences across strong edges. Propagation is a smoothed solve of that penalty with the seed labels as boundary conditions. The `alpha` parameter sets how far labels travel: near 0, each node stays close to its seed, and near 1, labels diffuse across the whole graph. Because the normalization uses degrees, a hub node does not dominate the spread by sheer edge count.

### Where this shows up in production

Label propagation shows up wherever relations are cheap and labels are expensive: spreading a few confirmed fraud accounts across a shared-device or payment graph, propagating product categories across co-purchase graphs, and extending a small set of moderated posts across near-duplicate content. The output is a score per node, which is then thresholded or ranked for review.

### Using it to make decisions

Use it when you can build a meaningful similarity graph, such as a kNN graph on good embeddings. Choose `alpha` on a validation set of labeled nodes that you hide during propagation. Check the graph first: if it has disconnected components with no seeds, those nodes will score zero everywhere, so count them before you trust the output. Tune the kNN size because too few neighbours fragment the graph and too many blur classes together.

### Pros and cons

**Pros:** works with very few labels, uses unlabeled structure directly, and is a simple linear-algebra iteration with a clear closed form.

**Cons:** quality depends entirely on the graph, which is costly to build at scale, memory grows with the number of edges, and nodes in unseeded components get no information.

## Explanation

The solution normalizes the affinity matrix once and then iterates the update, which converges to the closed form because the spectral radius of `alpha S` is below one. Checking the input structure up front means a bad graph fails loudly instead of producing a plausible-looking but meaningless score.
