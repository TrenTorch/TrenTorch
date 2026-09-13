---
name: decision-trees-best-split-minimal-tree
title: Decision Tree best split (assemble a minimal tree)
tags: [classical-ml, decision-trees, tree-building]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-gini-impurity` scores a node and `02-information-gain` scores one proposed split. A usable tree must search all meaningful splits, choose the strongest improving one, then repeat independently on the two groups it creates. It also needs clear stopping rules so it does not keep memorizing smaller and smaller groups.

### From theory to code

Implement `find_best_split`, `build_tree`, and `predict_tree`. Theory maps candidate midpoints to the gain search, the recursive nested-dictionary representation, and the traversal rule used at inference.

### Constraints

- `input` is `(n_samples, n_features)` and `labels` is `(n_samples,)`.
- Search each feature's midpoints between consecutive unique values; use `<= threshold` for the left child.
- Return `(feature, threshold, gain)` only for a strictly positive best gain; otherwise return `None`.
- Stop recursion at `max_depth == 0`, fewer than two labels, a pure node, or no improving split.
- Leaves use the majority class; split nodes contain `feature`, `threshold`, `left`, and `right`.
- `predict_tree` returns an integer label per input row; tree construction and prediction may loop because they follow data-dependent branches.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Only a boundary between two distinct observed feature values can change which samples reach each child.

</details>

<details><summary>Hint 2</summary>

Initialize the best gain to `0.0`; update all three best-split fields only when a candidate is strictly better.

</details>

<details><summary>Hint 3</summary>

At a leaf, return the label whose count is largest. At a split, reuse its stored feature and threshold to create the two recursive calls and later to route a prediction.

</details>

## Theory

### The simple version

A tree repeatedly asks the most clarifying yes-or-no question available. Every answer sends an example into a smaller group, where the next question can be tailored to that group. If no question improves the mixture or the depth budget is gone, the group votes as a leaf.

### The formula

For feature `j`, sort its distinct present values `v`. Its candidates are:

```text
thresholds = (v[:-1] + v[1:]) / 2
gain(j, t) = information_gain(labels, labels[input[:, j] <= t], labels[input[:, j] > t])
```

Choose the candidate with greatest positive gain. A node is either:

```text
leaf:  {"leaf": True, "prediction": majority_class(labels)}
split: {"leaf": False, "feature": j, "threshold": t,
        "left": build_tree(left, depth-1), "right": build_tree(right, depth-1)}
```

Prediction follows `<= threshold` left and `> threshold` right until reaching a leaf.

### How PyTorch actually implements this

Context only, untested by your submission: this is a greedy CART-style search rather than a `torch.nn` tensor layer. The tests include an offline-generated scikit-learn `DecisionTreeClassifier` training-accuracy oracle for a fixed depth-three dataset.

## Explanation

`find_best_split` gets sorted distinct `values` with `np.unique`, skips constant features, and computes every adjacent midpoint. Each threshold creates `left_mask`; `information_gain` receives the matching label subsets. Starting at `best_gain = 0.0` means zero-gain cases such as XOR return `None`. `_majority_class` counts labels using `np.unique` and chooses `values[np.argmax(counts)]`.

`build_tree` checks depth, sample count, and `gini_impurity(labels)` before searching. A missing split also becomes a majority-vote leaf; otherwise the stored mask recursively builds both subtrees with `max_depth - 1`. `predict_tree` allocates integer `predictions`, then walks each row's `node` through the same inclusive threshold rule until assigning its leaf prediction.
