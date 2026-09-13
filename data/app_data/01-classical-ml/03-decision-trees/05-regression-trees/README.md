---
name: decision-trees-regression-trees
title: 'Regression trees: splitting on variance reduction instead of Gini'
tags: [classical-ml, decision-trees, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Classification trees group labels; regression trees group real-valued targets. A good numeric leaf is one whose targets can be represented by a single useful number, so this version measures spread rather than class mixing. The split search and recursion stay familiar, but leaves must predict means and predictions must remain floating-point values.

### From theory to code

Implement `variance`, `variance_reduction`, `find_best_regression_split`, `build_regression_tree`, and `predict_regression_tree`. Theory translates each classification-tree operation into its continuous-target counterpart.

### Constraints

- `targets` are real-valued; empty `targets` have variance `0.0`.
- Weight child variances by their sample counts when computing reduction.
- Search every feature's adjacent-unique-value midpoint and return `None` without a positive reduction.
- Stop building at depth zero, fewer than two targets, zero variance, or no valid split.
- A leaf stores `float(np.mean(targets))`, never a class vote.
- Return a float prediction array and traverse each row using the stored inclusive threshold.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Everything about candidate thresholds is the same as the classification tree; only the node-quality measure changes.

</details>

<details><summary>Hint 2</summary>

`np.var` gives the population variance required here. For an empty input, return before calling it.

</details>

## Theory

### The simple version

A regression leaf predicts one number for every target it contains. Variance measures how poor that one-number summary is. A split is useful when its two child averages describe their targets with much less spread than the parent average did.

### The formula

```text
variance(y) = mean((y - mean(y)) ** 2)
reduction = variance(parent)
          - (n_left / n) * variance(left)
          - (n_right / n) * variance(right)
```

The best positive-reduction midpoint becomes a split. A terminal node returns `prediction = mean(targets)`, the constant that minimizes squared error in that node.

### How PyTorch actually implements this

Context only, untested by your submission: this is a CART-style regression-tree procedure rather than a core PyTorch layer. The tests contain an offline-generated scikit-learn `DecisionTreeRegressor(criterion='squared_error')` training-MSE oracle for the same fixed dataset.

## Explanation

`variance` guards `targets.size == 0` before returning `float(np.var(targets))`. `variance_reduction` mirrors information gain exactly but calls `variance`, weighting both child values by `child.size / n_samples`.

`find_best_regression_split` initializes `best_reduction` to `0.0`, loops over unique-value midpoints, and records only strictly larger reductions. `build_regression_tree` changes the classification purity check to `variance(targets) == 0.0` and every leaf uses `float(np.mean(targets))`. `predict_regression_tree` deliberately allocates `predictions` with `dtype=float`; its row-by-row path logic is otherwise the same inclusive comparison used for classification trees.
