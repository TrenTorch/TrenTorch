---
name: evaluation-bias-variance-tradeoff
title: 'Bias-variance tradeoff'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

Implement:

```python
def polynomial_features(x, degree) -> np.ndarray: ...
def fit_polynomial(x, y, degree) -> np.ndarray: ...
def predict_polynomial(coefficients, x) -> np.ndarray: ...
def bias_variance_decomposition(predictions, targets) -> tuple[float, float, float]: ...
```

- `predictions` in `bias_variance_decomposition` is many independently-trained models' predictions on the _same_ test points, one row per model, `targets` is the true, noiseless function value at each test point (not a noisy training label).

## Theory

Every model built in this curriculum has a real, unavoidable tension: a model too simple to capture the true pattern (**high bias**, systematically wrong in the same way no matter how much data it sees) versus a model so flexible it fits the specific noise in whatever training set it happened to see (**high variance**, wildly different predictions depending on which training sample it got).

Squared-error expected test error decomposes exactly into these two pieces (plus irreducible noise, ignored here by comparing against the _true_, noiseless function):

```text
expected error = bias^2 + variance

bias^2   = (average prediction across many differently-trained models - true value)^2
variance = how much those models' predictions disagree with EACH OTHER, on the same test point
```

A degree-1 (linear) polynomial fit to a genuinely curved function (like `sin(x)`) can't represent the curve no matter how much training data it gets, high, unavoidable bias, but a straight line fit to different random training samples looks nearly the same each time, low variance. A degree-15 polynomial fit to only 20 noisy training points can wiggle through the noise almost perfectly, low bias on the training data it saw, but a completely different squiggly curve for a different random training sample, high variance. Neither extreme wins, the actual goal is the complexity level that minimizes their sum, not either piece alone.

## Explanation

`polynomial_features(x, degree)` builds the same kind of Vandermonde-style design matrix a polynomial regression needs, `[1, x, x^2, ..., x^degree]` per row, via `np.stack([x**d for d in range(degree+1)], axis=1)`.

`fit_polynomial` calls `np.linalg.lstsq` (least-squares, the closed-form solution rather than an iterative gradient-descent loop, since this design matrix is small and well-suited to a direct solve) against that design matrix, returning the fitted coefficients. `predict_polynomial` infers `degree` back out from `len(coefficients) - 1` and evaluates the same polynomial at new `x` values, `design_matrix @ coefficients`.

`bias_variance_decomposition` computes `mean_prediction = predictions.mean(axis=0)`, the "average model's" prediction at each test point, across every independently-trained model. `bias_squared` compares that average prediction against the true value, squared-error, averaged over test points, exactly what "systematically wrong" means. `variance` is `predictions.var(axis=0)`, how much the individual models' predictions spread out around their own mean at each test point, averaged the same way, exactly what "wildly different depending on training data" means.
