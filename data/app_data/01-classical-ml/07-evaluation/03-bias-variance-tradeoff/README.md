---
name: evaluation-bias-variance-tradeoff
title: 'Bias-variance tradeoff'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-classification-metrics` measures how wrong a model's predictions are on average. It doesn't explain *why* a model is wrong. A model too simple to represent the true pattern will be wrong the same way on every training set it's given — that's bias. A model flexible enough to chase the specific noise in whatever training set it happened to see will be wrong differently every time — that's variance. Two models can have the same average test error for completely different reasons, and knowing which reason applies is what tells you whether to make the model *more* flexible or *less*.

This is the same tension every model in this curriculum faces implicitly, from a straight-line fit to a deep tree: too rigid and it can't capture the pattern regardless of data; too flexible and it fits each dataset's particular noise instead of the pattern underneath.

### From theory to code

Implement `polynomial_features`, `fit_polynomial`, and `predict_polynomial` to produce many independently-trained polynomial fits of varying complexity, then `bias_variance_decomposition(predictions, targets)` to split their collective test error into the two pieces Theory separates.

### Constraints

- `polynomial_features(x, degree)`: returns shape `(n_samples, degree+1)`, columns `1, x, x^2, ..., x^degree`.
- `fit_polynomial(x, y, degree)`: least-squares fit, returns coefficients of shape `(degree+1,)`.
- `predict_polynomial(coefficients, x)`: evaluates a fitted polynomial at new `x` values; `degree` is inferred from `coefficients`, not passed separately.
- `bias_variance_decomposition(predictions, targets)`: `predictions` has shape `(n_models, n_test_points)`, one row per independently-trained model's predictions on the *same* test points; `targets` has shape `(n_test_points,)`, the true, noiseless function value at each point (not a noisy training label).
- Returns `(bias_squared, variance, bias_squared + variance)`, each averaged over test points.
- `variance` measures disagreement *across models* at each test point, not across test points for one model — the two axes are not interchangeable.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`polynomial_features` is a Vandermonde-style design matrix: stack `x**d` for `d` from `0` to `degree` as columns. `fit_polynomial` and `predict_polynomial` both go through that same matrix — build it once, reuse it.

</details>

<details>
<summary>Hint 2</summary>

`bias_variance_decomposition`'s `predictions` array has one row per model and one column per test point. The "average model" at a given test point is a mean *down* a column (`axis=0`), not across a row.

</details>

<details>
<summary>Hint 3</summary>

Bias compares that per-point average prediction to the true value, squared, then averaged over points. Variance is how much each model's prediction at a point spreads around *that point's own average*, i.e. `predictions.var(axis=0)`, again averaged over points.

</details>

## Theory

### The simple version

Imagine several archers, each firing many arrows at the same target, but each archer using a different, slightly-wrong training set to calibrate their aim. If every archer's arrows cluster tightly but consistently off to one side, that's bias — the aiming method itself is flawed, more practice won't fix it. If every archer's arrows scatter wildly in different directions depending on which practice session they had, that's variance — the aiming method is sensitive to noise in whatever data it was calibrated on.

A degree-1 (straight-line) fit to a genuinely curved function like `sin(x)` can't represent the curve no matter how much training data it sees — high, unavoidable bias — but a straight line fit to different random samples looks nearly the same each time — low variance. A degree-9 polynomial fit to only 20 noisy points can wiggle through the specific noise almost perfectly on the data it saw — low bias there — but produces a wildly different squiggly curve for a different random sample — high variance. The actual goal is whatever complexity minimizes the *sum*, not either piece alone.

### The formula

```text
expected squared error = bias^2 + variance   (ignoring irreducible noise, since targets here are the true noiseless function)

mean_prediction = predictions.mean(axis=0)                  # per test point, across models
bias_squared    = mean((mean_prediction - targets) ** 2)     # averaged over test points
variance        = mean(predictions.var(axis=0))              # per-point spread across models, averaged over test points
```

### How PyTorch actually implements this

Context only, untested by your submission: this decomposition is a diagnostic computed from many trained models' outputs, not a `torch.nn` layer or loss function. `fit_polynomial`'s least-squares solve corresponds to `torch.linalg.lstsq`; there's no PyTorch primitive for the bias/variance split itself, it's just `.mean()`/`.var()` calls on a tensor of stacked predictions.

## Explanation

`polynomial_features(x, degree)` builds the design matrix via `np.stack([x**d for d in range(degree+1)], axis=1)` — column `d` is `x` raised to the `d`-th power, exactly the `[1, x, x^2, ..., x^degree]` per-row layout a polynomial regression needs.

`fit_polynomial` calls `polynomial_features(x, degree)` then `np.linalg.lstsq(design_matrix, y, rcond=None)` — the closed-form least-squares solution rather than an iterative gradient-descent loop, since this design matrix is small and well-suited to a direct solve — and returns the fitted `coefficients`. `predict_polynomial` infers `degree = coefficients.shape[0] - 1` (no separate `degree` argument needed, since the coefficient count fixes it) and evaluates `design_matrix @ coefficients` at the new `x` values.

`bias_variance_decomposition` computes `mean_prediction = predictions.mean(axis=0)` — the "average model's" prediction at each test point, averaged down the model axis. `bias_squared = mean((mean_prediction - targets) ** 2)` compares that average prediction against the true value, exactly what "systematically wrong" means. `variance = mean(predictions.var(axis=0))` takes the variance *down each column* (across models, at a fixed test point) before averaging across points — `test_variance_is_computed_across_models_not_across_test_points` exists specifically because averaging along the wrong axis (`axis=1`) would report `0` variance for models whose predictions are constant across test points but wildly different from each other, exactly backwards from what variance is meant to capture here.
