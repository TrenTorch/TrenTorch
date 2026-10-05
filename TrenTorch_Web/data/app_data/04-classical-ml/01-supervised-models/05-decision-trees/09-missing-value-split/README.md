---
name: decision-tree-missing-value-split
title: 'Split gain with missing feature values'
tags: [classical-ml, decision-trees, missing-values, information-gain]
difficulty: Intermediate
---

## Statement

### Score a threshold split when some rows have no value

A tree split on a numeric feature `x` needs a value for every row. Real data has gaps, so the C4.5 approach scores the split on the rows that have a value, then scales the gain by the fraction of rows that are known. Rows with a missing value are sent down both branches later, weighted by how the known rows fell.

Implement `fractional_split_gain(x, y, threshold)`, where `x` is a 1-D float array that may contain `NaN`, and `y` holds integer class labels.

- Let `known` be the rows where `x` is not `NaN`, and let `F = |known| / n`.
- Left branch: known rows with `x <= threshold`. Right branch: the other known rows.
- `gain = F * (H(parent) - weighted child entropy)`, where `H` uses base-2 logs and the parent and children are computed on known rows only.
- Return `(gain, p_left)`, where `p_left` is the fraction of known rows that went left.

### Constraints

- `x` and `y` must be 1-D with the same length. Otherwise raise `ValueError`.
- If every value of `x` is `NaN`, raise `ValueError`.
- A split that sends every known row to one side has gain `0`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute `p_left` and the gain from the same boolean mask, then reuse the entropy helper for both children.

</details>

## Theory

Information gain measures how much a split reduces label entropy. When part of the feature is missing, the gain on the known rows is biased upward relative to a split that has complete data, because the missing rows carry no information about the split. Scaling by `F` penalizes that. The fraction `p_left` is then the routing weight that a missing-value row takes into the left branch at prediction time.

### Where this shows up in production

Tree libraries handle missing values in several ways. XGBoost learns a default direction per split from the training data, and LightGBM does the same. Scikit-learn added native missing-value support to its histogram trees, which learn the default side from the training data. The C4.5 style fractional approach is what you rebuild when you write a tree from scratch for an embedded or regulated environment.

### Using it to make decisions

Use the scaled gain to compare thresholds on the same feature, where the set of missing rows is the same. Be careful when comparing features, because a feature with 40% missing values is scaled down by `0.6`, which is usually the correct penalty but can hide a useful column. Before you trust a split, check that the missingness itself is not informative. If a missing value means something (a field that is only filled for premium users), add an explicit indicator column instead of relying on routing.

### Pros and cons

**Pros:** the rule is simple, uses only observed rows to find the split, and the penalty makes features with heavy missingness less attractive by default.

**Cons:** the rule can hide that missingness itself carries signal. The routing weight `p_left` is a summary, so rows with missing values get a probabilistic route rather than a learned one. Each threshold needs a full pass over the data.

## Explanation

The solution masks out the `NaN` rows, computes the entropy of the parent and of each child on the known rows, and scales the result by the known fraction. The routing weight comes from the same boolean mask, so the two outputs always agree.
