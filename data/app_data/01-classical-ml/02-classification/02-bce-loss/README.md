---
name: classification-bce-loss
title: Binary Cross-Entropy Loss
tags: [classical-ml, classification, loss-functions]
difficulty: Beginner
---

## Statement

Implement:

```python
def bce_loss(p: np.ndarray, y: np.ndarray) -> float:
    """
    p: predicted probabilities, shape (n_samples,)
    y: true labels (0 or 1), shape (n_samples,)
    Returns a single scalar.
    """
```

Your function should:

1. Clip `p` away from exactly 0 or 1 before taking a log.
2. Return the mean BCE across all samples as a Python float.

## Theory

MSE doesn't punish a confidently wrong probability nearly hard enough.

```text
L = -mean( y*log(p) + (1-y)*log(1-p) )
```

- when `y = 1`, loss is `-log(p)` — grows huge as `p` approaches 0.
- when `y = 0`, loss is `-log(1-p)` — grows huge as `p` approaches 1.

## Explanation

The clip bound `1e-12` isn't arbitrary comfort padding — without it, a prediction that legitimately rounds to exactly `0.0` or `1.0` in float64 (which happens after enough training) makes `log(0)` return `-inf`, and the loss becomes `nan` on the next line's arithmetic. `1e-12` is far enough from 0/1 to never distort a real prediction's loss value, but close enough that clipping only ever triggers on the genuinely-saturated case it exists for.
