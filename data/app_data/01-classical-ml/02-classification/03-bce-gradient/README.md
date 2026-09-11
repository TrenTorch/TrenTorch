---
name: classification-bce-gradient
title: Gradient of BCE
tags: [classical-ml, classification, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

Implement:

```python
def bce_grad(X: np.ndarray, p: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Returns:
        dw: gradient with respect to w
        db: gradient with respect to b
    """
```

## Theory

The gradient of BCE with respect to the raw linear score `z` simplifies to exactly:

```text
dL/dz = p - y
dw = (1/n) X.T @ (p - y)
db = (1/n) sum(p - y)
```

The same "prediction minus target" shape as Linear Regression's residual, built on top of a different upstream function.

## Explanation

Note the `1/n` here, not Linear Regression's `2/n` — BCE's derivative doesn't carry MSE's factor-of-2 from squaring, since `d/dp[-log(p)] = -1/p` has no square to differentiate through. Copy-pasting Linear Regression's gradient scaling here would silently train at half the intended learning rate, a bug the finite-difference test below would catch but a hardcoded-example test alone might not, depending on the example chosen.
