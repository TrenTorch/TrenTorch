---
name: ensembles-extra-trees-random-split
title: 'Extra-trees random split'
tags: [classical-ml, supervised, ensembles, decision-tree, randomization]
difficulty: Intermediate
---

## Statement

### Pick the threshold at random

A standard decision tree searches every candidate threshold for the best split. Extremely randomized trees skip that search: for a chosen feature they draw one threshold uniformly between the feature's minimum and maximum in the node, and keep the better of the random choices across features.

Implement `extra_tree_split(x, y, seed)` for one feature `x` and binary labels `y` in `{0, 1}`. Return `(threshold, gain)`.

1. Let `lo = x.min()` and `hi = x.max()`. If `lo == hi`, return `(None, 0.0)`.
2. Create `rng = np.random.default_rng(seed)` and set `threshold = rng.uniform(lo, hi)`.
3. Send rows with `x <= threshold` left and the rest right.
4. Gain is the Gini reduction: gini(y) − (n_L / n) · gini(y_L) − (n_R / n) · gini(y_R), where gini(p) = 1 − Σ p_c². If one side is empty, the gain is 0.0.

### Constraints

- `x` and `y` must have the same length, otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Use the exact call `rng.uniform(lo, hi)` so the threshold is reproducible from the seed.

</details>

## Theory

Random thresholds trade a little split quality for a lot of speed and extra variance reduction when many trees are averaged. The randomness decorrelates the trees, which is the point of the method.

## Explanation

The solution draws one uniform threshold from the seeded generator, partitions the node, and computes the Gini gain. Keeping the threshold draw as a single `rng.uniform` call makes the behavior easy to check exactly.
