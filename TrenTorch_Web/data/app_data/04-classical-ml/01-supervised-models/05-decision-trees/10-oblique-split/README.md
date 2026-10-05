---
name: decision-tree-oblique-split
title: 'Oblique split gain'
tags: [classical-ml, decision-trees, oblique-splits, gini]
difficulty: Advanced
---

## Statement

### Score a split along a slanted direction

An axis-aligned tree asks one question per node: is feature `j` at most `t`? An oblique tree asks about a linear combination instead: is `w . x + b <= 0`? That lets one node cut a diagonal boundary that would otherwise need a staircase of splits.

Implement `oblique_split_gain(X, y, w, b)` that scores this split with Gini impurity.

- `X` is an `n` by `d` float matrix, `y` holds integer labels of length `n`, `w` has length `d`, and `b` is a scalar.
- Left branch: rows where `X @ w + b <= 0`. Right branch: the rest.
- Return `G(parent) - (n_left / n) G(left) - (n_right / n) G(right)`, where `G = 1 - sum_c p_c^2`.

### Constraints

- `X` must be 2-D, `w` must have length `d`, and `y` must have length `n`. Otherwise raise `ValueError`.
- `w` must not be the zero vector. Raise `ValueError` in that case, because the direction is undefined.
- An empty child contributes zero impurity.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Scaling `w` and `b` by the same positive number does not change which side a row lands on, so the gain must be unchanged.

</details>

## Theory

Gini impurity of a node is the probability that two rows drawn at random from it have different labels. A split is good when the weighted impurity of its children falls. Oblique splits reuse this criterion, but the search space is continuous in the direction `w`, so libraries search over random directions or refine a direction with a linear model.

### Where this shows up in production

Oblique trees appear in random rotation forests, an ensemble method where each tree is grown on a randomly rotated copy of the features, and in oblique variants described in the tree-learning research literature. They are used where features are correlated and a single rotation of the input cuts a boundary that axis-aligned trees approximate poorly, such as in sensor fusion or in spectral data. They are also a stepping stone toward model-based trees that place a logistic regression in each node.

### Using it to make decisions

Use oblique splits when the axis-aligned tree is deep and still misclassifies along diagonal boundaries, and when the features are on comparable scales. Before deploying, measure the cost of the projection at every node, since each prediction now does a dot product per node rather than a single comparison. If interpretability matters, prefer a rotation applied once before an axis-aligned tree, because the rotated features can be named and audited.

### Pros and cons

**Pros:** one oblique split replaces a staircase of axis-aligned splits, so trees are often shallower and more accurate on correlated data.

**Cons:** each node is harder to explain, because the split is a weighted sum of features rather than one named threshold. Inference needs a dot product at every node, and the search over directions adds training cost. The gain is sensitive to feature scaling, so unscaled inputs make the chosen direction arbitrary.

## Explanation

The solution projects every row onto `w`, shifts by `b`, and splits on the sign. Gini impurity is computed for the parent and both children, and the gain is the drop in weighted impurity. Because the split depends only on the sign of `w . x + b`, scaling `w` and `b` together leaves the result unchanged.
