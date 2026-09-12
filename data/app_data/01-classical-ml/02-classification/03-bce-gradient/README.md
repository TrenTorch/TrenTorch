---
name: classification-bce-gradient
title: Gradient of BCE
tags: [classical-ml, classification, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

Implement:

```python
def bce_gradient(
    input: np.ndarray,
    p: np.ndarray,
    target: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    input:  shape (batch_size, in_features)
    p:      shape (batch_size, 1), sigmoid(linear(input, weight, bias))
    target: shape (batch_size, 1)

    Returns:
        grad_weight: shape (1, in_features)
        grad_bias: shape (1,)
    """
```

`p`/`target` follow `01-hypothesis-function`'s convention, `(batch_size, 1)`, never squeezed to `(batch_size,)`, so `grad_weight`/`grad_bias` come out matching `weight`'s `(1, in_features)` / `bias`'s `(1,)` shape directly, the same convention Linear Regression's `03-mse-gradient` uses.

## Theory

The gradient of BCE with respect to the raw linear score `z` simplifies to exactly:

```text
d(loss)/dz = p - target
grad_weight = (1/n) * (p - target).T @ input
grad_bias   = (1/n) * sum(p - target, axis=0)
```

The same "prediction minus target" shape as Linear Regression's residual, built on top of a different upstream function (`sigmoid` instead of the identity).

## Explanation

Note the `1/n` here, not Linear Regression's `2/n`, BCE's derivative doesn't carry MSE's factor-of-2 from squaring, since `d/dp[-log(p)] = -1/p` has no square to differentiate through. Copy-pasting Linear Regression's gradient scaling here would silently train at half the intended learning rate, a bug the finite-difference test below would catch but a hardcoded-example test alone might not, depending on the example chosen.

`error.T @ input` and `error.sum(axis=0)` are the exact same shape operations `03-mse-gradient` uses for `grad_weight`/`grad_bias`, keeping `error` (here `p - target`) as a `(batch_size, 1)` column throughout is what makes that reuse work without a reshape.
