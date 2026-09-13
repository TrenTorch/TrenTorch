---
name: decision-trees-feature-importance
title: Feature importance from a fitted tree
tags: [classical-ml, decision-trees, interpretability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A fitted tree reveals which feature questions reduced label uncertainty, but a feature may appear at several depths. Feature importance collects that evidence into one comparable score per original input feature while giving broad, high-level splits more credit than tiny late branches.

### From theory to code

Implement `feature_importances(tree, input, labels, n_features)`. Re-route the original training data through the stored tree, compute each split's gain, accumulate its sample-weighted credit, and normalize the result.

### Constraints

- `tree` was fit on the supplied `input` and `labels`; `n_features` is the full input width.
- Return shape `(n_features,)`.
- Recreate each node's subsets using its stored feature, threshold, and inclusive left rule.
- Add `(node_labels.size / total_samples) * information_gain(...)` to the split feature.
- Normalize only when the sum is positive; a single leaf returns all zeros.
- Reuse `information_gain` and do not mutate the tree or data.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The tree stores split decisions, not the data that reached them; carry a data subset through a recursive walk.

</details>

<details><summary>Hint 2</summary>

At a split node, form `left_mask` from that node's feature and threshold, recurse on both masked subsets, and credit the current feature before recursing.

</details>

## Theory

### The simple version

Importance is a feature's share of the tree's useful decisions. A root split helped every sample, while a deep split only helped samples that survived earlier questions, so each gain is discounted by the fraction of the dataset it touched.

### The formula

```text
gain = information_gain(node_labels, left_labels, right_labels)
weight = node_labels.size / total_samples
importances[feature] += weight * gain
```

After walking all non-leaf nodes, return `importances / importances.sum()` when the sum is positive; otherwise return the zero array.

### How PyTorch actually implements this

Context only, untested by your submission: this is the Gini mean-decrease-in-impurity calculation commonly exposed by tree libraries, not a core `torch.nn` operation. The tests include an offline-generated scikit-learn feature-importance oracle.

## Explanation

`importances = np.zeros(n_features)` provides one accumulator per original feature, while `total_samples = labels.size` stays fixed for all node weights. The nested `walk` stops at leaves. For every split it computes `left_mask` from the stored `feature` and `threshold`, recreates child labels, obtains `gain`, and adds `weight * gain` to `importances[feature]` before recursively carrying the matching input and label subsets.

After `walk(tree, input, labels)`, `total = importances.sum()` guards the normalization. A one-leaf tree has no credited gain and returns all zeros; otherwise division makes the feature scores sum to one.
