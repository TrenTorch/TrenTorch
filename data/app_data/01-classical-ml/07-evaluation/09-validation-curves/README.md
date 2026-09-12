---
name: evaluation-validation-curves
title: 'Validation curves: training/validation error vs. one hyperparameter'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

Implement:

```python
def validation_curve(fit_and_evaluate_fn, param_values) -> tuple[np.ndarray, np.ndarray]:
    """fit_and_evaluate_fn(param_value) -> (train_error, val_error)."""
```

## Theory

`08-learning-curves` fixed the model and swept the _amount of data_. A validation curve fixes the _amount of data_ and sweeps one hyperparameter instead, directly visualizing the complexity side of the bias-variance tradeoff (`03-bias-variance-tradeoff`) as one number changes.

```text
param_values: 1, 2, 3, 5, 7, 9, 12   (e.g. polynomial degree, max_depth, n_trees...)
   ↓ for each value, train on the SAME fixed training set, measure both errors
train_errors, val_errors, one pair per value
```

The classic shape: training error decreases (often close to monotonically) as the hyperparameter increases model complexity, a more flexible model fits its training set better, almost by definition. Validation error, though, typically forms a **U-shape**: too little complexity underfits (both errors high, `03-bias-variance-tradeoff`'s high-bias regime), too much complexity overfits (training error keeps dropping, but validation error turns around and climbs, high variance), and the bottom of the U is the sweet spot, the actual best value to pick for this hyperparameter.

```text
error
  |  val: high \                    / high (overfitting climbs back up)
  |          \                    /
  |           \___low (sweet spot, the U's bottom)
  |  train:          \___________________ (keeps dropping)
  +-------------------------------------------- complexity →
```

This is exactly what `04-grid-search`/`05-random-search` are trying to find automatically, a validation curve is the same search made visible for one hyperparameter at a time, useful for understanding _why_ a search landed where it did, not just what it picked.

## Explanation

`validation_curve` is structurally identical to `08-learning-curves`'s `learning_curve`, a loop calling `fit_and_evaluate_fn` once per entry in `param_values` and collecting the two returned errors, the only difference is what varies between calls: a hyperparameter value here, a training-set size there. Both leave the actual training and evaluation to the caller-supplied function, this question is purely about the sweep.
