---
name: linear-regression-mse-gradient
title: Gradient of MSE with Respect to w and b
tags: [classical-ml, linear-regression, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

Implement:

```python
def mse_grad(
    X: np.ndarray,
    y_hat: np.ndarray,
    y: np.ndarray
) -> tuple[np.ndarray, float]:
    """
    Returns:
        dw: gradient with respect to w
        db: gradient with respect to b
    """
```

Use the formulas:

```text
dw = (2/n) * X.T @ (y_hat - y)
db = (2/n) * sum(y_hat - y)
```

Do not use an autograd library.

## Theory

We can now make predictions and measure their error.

But we still have a problem:

How do we change `w` and `b` so that the loss becomes smaller?

This is where the gradient comes in.

The gradient tells us how the loss changes when we change the parameters.

For MSE, the gradients are:

```text
dL/dw = (2/n) Xᵀ(ŷ - y)
dL/db = (2/n) Σ(ŷ - y)
```

So:

- `dw` tells us how each weight affects the loss.
- `db` tells us how the bias affects the loss.

This gives us the missing connection:

```text
X, w, b
   ↓
prediction
   ↓
loss
   ↓
gradient
   ↓
how should w and b change?
```

For this track, you will calculate these derivatives manually rather than using automatic differentiation.

## Explanation

`error = y_hat - y` is computed once and reused for both `dw` and `db`, instead of recomputing the subtraction twice.

`X.T @ error`, not `error @ X.T` — get this backwards and `dw` comes out with the _wrong shape entirely_ rather than a subtly wrong value, which is why a dedicated shape test exists separate from the numeric ones.

`db` gets the same `float(...)` treatment as `mse_loss`, for the same reason: `np.sum` returns a NumPy scalar, not a Python float.
