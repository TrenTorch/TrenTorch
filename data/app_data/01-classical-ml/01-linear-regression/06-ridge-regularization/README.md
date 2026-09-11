---
name: linear-regression-ridge-gradient
title: 'Stretch: L2 Regularization (Ridge)'
tags: [classical-ml, linear-regression, regularization, stretch]
difficulty: Intermediate
---

## Statement

Implement:

```python
def ridge_grad(
    X: np.ndarray,
    y_hat: np.ndarray,
    y: np.ndarray,
    w: np.ndarray,
    lam: float
) -> tuple[np.ndarray, float]:
    """
    Compute the gradient of the MSE loss with L2 regularization.
    """
```

Your function should:

1. Compute the base MSE gradient using the same formula as the earlier gradient question.
2. Extend just the _weight_ gradient with the additional penalty term derived in Theory — one that grows with both the weight's own magnitude and `lam`.
3. Leave the bias gradient untouched — bias is never regularized.

## Theory

So far, the model only cares about fitting the training data.

Sometimes we also want to discourage the model from using very large weights.

We can do that by adding a penalty to the objective:

```text
L_ridge = MSE + λ Σw²
```

where `λ` controls how strongly large weights are penalized.

The corresponding gradient becomes:

```text
dw_ridge = dw_mse + 2λw
db_ridge = db_mse
```

The bias is not regularized.

```text
larger λ
   ↓
stronger penalty on large weights
   ↓
smaller learned weights
```

This is called L2 regularization or weight decay in this setting.

## Explanation

Calls `mse_grad(X, y_hat, y)` rather than reimplementing the base gradient inline — same "wire, don't reimplement" discipline as the training-loop question.

Only `dw` gets `+ 2 * lam * w`; `db` is returned untouched straight from `mse_grad`, which is what actually _enforces_ "bias is never regularized" rather than just asserting it in a comment.
