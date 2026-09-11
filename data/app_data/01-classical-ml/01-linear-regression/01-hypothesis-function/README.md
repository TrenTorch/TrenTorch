---
name: linear-regression-hypothesis-function
title: Hypothesis Function
tags: [classical-ml, linear-regression, forward-pass]
difficulty: Beginner
---

## Statement

Implement:

```python
def linear_forward(
    X: np.ndarray,
    w: np.ndarray,
    b: float
) -> np.ndarray:
    """
    X: shape (n_samples, n_features)
    w: shape (n_features,)
    b: scalar

    Returns:
        Predictions with shape (n_samples,)
    """
```

Your function should:

1. Return exactly one prediction per sample, using the rule derived in Theory.
2. Support any number of features, including exactly one.
3. Compute all samples in a single vectorized expression — no Python `for` loop over samples.
4. Preserve `X`'s dtype in the output (don't hardcode `float32`/`float64`).

## Theory

A model needs a rule for turning inputs into predictions.

In linear regression, that rule is:

```text
ŷ = Xw + b
```

Here:

- `X` contains the input features.
- `w` contains one weight for each feature.
- `b` is the bias.
- `ŷ` is the prediction made by the model.

For one example with two features:

```text
ŷ = x₁w₁ + x₂w₂ + b
```

For many examples, matrix multiplication lets us calculate all predictions at once:

```text
ŷ = X @ w + b
```

This equation is called the hypothesis function.

Important: at this point, we are only defining what the model can represent. We have not learned the values of `w` and `b` yet.

## Explanation

`X @ w` relies on NumPy matmul treating a 1-D `(n_features,)` array on the right as a column vector, so it broadcasts against `(n_samples, n_features)` and produces `(n_samples,)` directly — no reshape needed. Adding scalar `b` broadcasts across every sample for free.

No dtype cast happens anywhere on purpose: whatever dtype `X` arrives in passes straight through, which is what "preserve dtype" in the requirements actually meant.
