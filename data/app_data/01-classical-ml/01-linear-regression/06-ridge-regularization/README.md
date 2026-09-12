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
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
    lam: float,
) -> tuple[np.ndarray, np.ndarray | None]:
    """
    Compute the gradient of the MSE loss with L2 regularization.
    """
```

Your function should:

1. Compute the base MSE gradient using `03-mse-gradient`'s `mse_gradient`.
2. Extend just the _weight_ gradient with the additional penalty term derived in Theory, one that grows with both the weight's own magnitude and `lam`.
3. Leave the bias gradient untouched, bias is never regularized, including the `bias is None` case.

## Theory

So far, the model only cares about fitting the training data. Sometimes we also want to discourage the model from using very large weights.

We can do that by adding a penalty to the objective:

```text
L_ridge = MSE + λ Σ weight²
```

where `λ` controls how strongly large weights are penalized. The corresponding gradient becomes:

```text
grad_weight_ridge = grad_weight_mse + 2λ * weight
grad_bias_ridge    = grad_bias_mse
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

Calls `mse_gradient(input, weight, bias, target)` rather than reimplementing the base gradient inline, same "wire, don't reimplement" discipline as `05-training-loop`.

Only `grad_weight` gets `+ 2 * lam * weight`; `grad_bias` is returned untouched straight from `mse_gradient`, unchanged and unconditionally, including when it's `None`, which is what actually enforces "bias is never regularized" rather than just asserting it in a comment.
