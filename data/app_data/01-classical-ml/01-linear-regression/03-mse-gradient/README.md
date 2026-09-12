---
name: linear-regression-mse-gradient
title: Gradient of MSE with Respect to w and b
tags: [classical-ml, linear-regression, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

Implement:

```python
def mse_gradient(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
) -> tuple[np.ndarray, np.ndarray | None]:
    """
    input:  shape (batch_size, in_features)
    weight: shape (out_features, in_features)
    bias:   shape (out_features,), or None
    target: shape (batch_size, out_features)

    Returns:
        grad_weight: same shape as weight
        grad_bias: same shape as bias, or None if bias is None
    """
```

Use the same forward pass as `01-hypothesis-function`'s `linear`, mean-reduced over every element the way `02-mse-loss` reduces.

Do not use an autograd library. These are the manual derivatives.

## Theory

`01-hypothesis-function` computed a prediction. `02-mse-loss` scored how wrong it was. Neither tells you which way to move `weight` and `bias` to make that score smaller, that's the gradient.

For mean-reduced MSE, `loss = (1/N) * sum((prediction - target)**2)` where `N` is the total element count (`batch_size * out_features`):

```text
d(loss)/d(prediction) = (2/N) * (prediction - target)
d(loss)/d(weight)     = d(loss)/d(prediction).T @ input
d(loss)/d(bias)       = sum(d(loss)/d(prediction), axis=0)
```

`weight`'s gradient is a matrix product because `weight` interacts with `input`. `bias`'s gradient is a plain sum because `bias` is added identically to every row, it doesn't interact with anything else.

If `bias` is `None`, there's no bias parameter to have a gradient, return `None`, not a zero array standing in for it, same distinction `01-hypothesis-function` draws for the forward pass.

This is exactly what `loss.backward()` computes automatically once autograd is introduced later in the curriculum: it walks the same chain rule, mechanically, instead of you writing it by hand.

## Explanation

`prediction = input @ weight.T` (plus `bias` if given) recomputes the forward pass, since the gradient is evaluated at the current parameter values, not some other point.

`grad_prediction = (2 / element_count) * (prediction - target)` is `d(loss)/d(prediction)`, derived from differentiating the mean of squares.

`grad_weight = grad_prediction.T @ input` and `grad_bias = grad_prediction.sum(axis=0)` push that back through the linear forward pass, the same shape rules `01-hypothesis-function` established for the forward direction, run in reverse.
