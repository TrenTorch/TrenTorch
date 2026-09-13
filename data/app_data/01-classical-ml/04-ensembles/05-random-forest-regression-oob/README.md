---
name: ensembles-random-forest-regression-oob
title: 'Random Forest regression, and out-of-bag error estimation'
tags: [classical-ml, ensembles, random-forest, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Bootstrap training leaves some rows out of every tree. For regression, tree outputs are averaged rather than voted, and the trees that omitted a row form a free, honest evaluation set for that row. This exercise records those omitted indices and uses only them for out-of-bag error.

### From theory to code

Implement bootstrap sampling with omitted indices, train a forest of `(tree, oob_indices)` pairs, average all tree predictions, and calculate OOB mean squared error.

### Constraints

- Bootstrap arrays have the original shapes and share one replacement-drawn index array.
- `oob_indices` contains original positions never drawn in that tree's bag.
- Train exactly `n_trees` with one advancing seeded generator.
- Regression forest prediction averages across trees along axis 0.
- OOB error uses only a sample's own OOB trees; samples with zero OOB predictions are excluded.
- Return OOB error as a Python float.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Mark every replacement-drawn index in a Boolean `in_bag` array; its inverse identifies omitted positions.

</details>

<details><summary>Hint 2</summary>

Keep one running OOB prediction sum and count per original row, then divide only where the count is positive.

</details>

## Theory

### The simple version

Each tree sees a different bag of training rows. A row a tree never saw can be treated like new data for that tree. Averaging only such unseen-tree opinions gives every covered row a built-in validation prediction.

### The formula

```text
in_bag[drawn_indices] = True
oob_indices = where(~in_bag)[0]
forest_prediction = mean(tree_predictions, axis=0)
oob_prediction[i] = sum(tree_i(input[i]) for i OOB) / OOB_count[i]
oob_error = mean((oob_prediction - target) ** 2) over OOB-covered rows
```

### How PyTorch actually implements this

Context only, untested by your submission: OOB evaluation is a bagged-tree technique typically implemented by tree libraries rather than `torch.nn`.

## Explanation

`bootstrap_sample_with_oob` draws replacement `indices`, marks them in Boolean `in_bag`, and gets sorted omitted indices with `np.where(~in_bag)[0]`. The training loop appends both each regression tree and its own OOB indices. Prediction stacks every `predict_regression_tree` result and uses `.mean(axis=0)`. `oob_error` maintains `oob_sums` and `oob_counts`, indexes only each tree's `oob_indices`, and filters with `has_oob_prediction` before computing the float MSE.
