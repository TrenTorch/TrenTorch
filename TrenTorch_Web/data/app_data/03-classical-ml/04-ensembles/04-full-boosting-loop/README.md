---
name: ensembles-full-boosting-loop
title: 'Full boosting loop: assemble a minimal booster'
tags: [classical-ml, ensembles, gradient-boosting]
difficulty: Advanced
---

## Statement

### The problem, from first principles

One residual tree makes one correction. A booster chains many such corrections, with each new tree seeing what every earlier tree still missed. The fitted model must also replay that same ordered, scaled sequence for unseen inputs.

### From theory to code

Implement `train_gradient_boosting` and `predict_gradient_boosting` using the existing residual-tree fitter and regression-tree predictor.

### Constraints

- Initialize with `float(np.mean(targets))` and one copy per training row.
- Fit exactly `n_trees` sequential residual trees; zero trees return an empty list.
- Scale every tree contribution by `learning_rate` during training and prediction.
- Return `(initial_prediction, trees)` and preserve tree order.
- Prediction starts from the same scalar for every new input row.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The next tree must observe the updated predictions, not the original constant prediction.

</details>

<details><summary>Hint 2</summary>

Training and inference differ only in where the initial prediction and trees came from; both add the same scaled tree outputs in order.

</details>

## Theory

### The simple version

The target mean is the best feature-free first guess. Each tree then takes a cautious step toward correcting the residuals left by the ensemble so far. Learning rate is the step size that makes each correction smaller.

### The formula

```text
initial = mean(targets)
predictions = full(n_samples, initial)
for each tree:
    tree = fit_tree_to_negative_gradient(input, targets, predictions, max_depth)
    predictions = predictions + learning_rate * predict_regression_tree(tree, input)
```

Inference repeats the final accumulation from `initial` over stored trees.

### How PyTorch actually implements this

Context only, untested by your submission: gradient boosting is normally a tree-library algorithm. The tests contain an offline-generated scikit-learn `GradientBoostingRegressor` oracle for the specified fixed dataset and hyperparameters.

## Explanation

`initial_prediction = float(np.mean(targets))` and `np.full` create the constant baseline. Each iteration calls `fit_tree_to_negative_gradient` with the current `predictions`, updates that array with `learning_rate * predict_regression_tree(tree, input)`, and appends the same tree. `predict_gradient_boosting` uses the identical `np.full` baseline and ordered update expression on its supplied input, which makes a zero learning rate leave the constant prediction unchanged.
