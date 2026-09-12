---
name: evaluation-learning-curves
title: 'Learning curves: training/validation error vs. dataset size'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

Implement:

```python
def learning_curve(fit_and_evaluate_fn, train_sizes) -> tuple[np.ndarray, np.ndarray]:
    """fit_and_evaluate_fn(n_samples) -> (train_error, val_error)."""
```

## Theory

`03-bias-variance-tradeoff` diagnosed underfitting versus overfitting by comparing many _differently-trained_ models against the truth. A learning curve diagnoses the same thing a different, more practical way: train the _same_ model (same hyperparameters, same complexity) on progressively more training data, and watch how training error and validation error move as the dataset grows.

```text
train_sizes: 10, 50, 100, 500, 1000, ...
   ↓ for each size, train on that many points, measure both errors
train_errors, val_errors, one pair per size
```

The shape of the two curves is a direct diagnosis:

- **High bias (underfitting)**: both curves plateau at a similarly high error, close together, and more data barely helps either one. The model is too simple to fit even the training data well, throwing more data at it doesn't fix that.
- **Good fit / high variance (overfitting) getting better with data**: training error stays low (a flexible model fits whatever training data it's given), validation error starts much higher but _decreases_ as training size grows and _converges toward_ the training error, more data narrows the gap between "what the model has seen" and "what it needs to generalize to."

This is a genuinely practical, checkable question a learning curve answers that `03-bias-variance-tradeoff`'s more abstract decomposition doesn't directly: "would collecting more training data actually help this specific model?" If the curves have already converged and plateaued, more data won't; if validation error is still visibly dropping, it might.

## Explanation

`learning_curve` is a thin loop over `train_sizes`, calling `fit_and_evaluate_fn(n_samples)` once per size and collecting the two returned error values into `train_errors`/`val_errors`. The actual work, training on a specific subset of the data and computing both errors, is left entirely to the caller-supplied `fit_and_evaluate_fn`, the same "black box function, don't assume what model it trains" pattern `04-grid-search`'s `fit_and_score_fn` uses, this question is purely about the sweep over dataset sizes, not about any specific model.
