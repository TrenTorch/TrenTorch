---
name: linear-regression-mse-loss
title: Mean Squared Error Loss
tags: [classical-ml, linear-regression, loss-functions]
difficulty: Beginner
---

## Statement

Implement:

```python
def mse_loss(
    y_hat: np.ndarray,
    y: np.ndarray
) -> float:
    """
    Returns the mean squared error as a single scalar.
    """
```

Your function should:

1. Reduce the per-sample errors down to one number summarizing overall model quality — smaller is better.
2. Return a plain Python `float`, not a NumPy scalar type or a 0-d array.
3. Work for any equal-length `y_hat`/`y`, including length 1.

## Theory

The model can now make predictions, but we need a way to answer:

"How wrong are these predictions?"

That is the job of a loss function.

For linear regression, we use Mean Squared Error (MSE):

```text
L = mean((ŷ - y)²)
```

where:

- `ŷ` = predictions;
- `y` = true targets;
- `ŷ - y` = prediction error.

We square each error so that positive and negative errors do not cancel out, and large errors are penalized more strongly.

So the process is now:

```text
X → linear model → ŷ → compare with y → loss
```

The loss is a single number telling us how well the current values of `w` and `b` are performing.

## Explanation

`np.mean(...)` returns `np.float64`, not a Python `float` — the `float(...)` wrapper isn't decoration, it's the actual fix for "must return a plain float."

`(y_hat - y) ** 2` computes every sample's squared error in one vectorized pass before the mean collapses it to a single number — no intermediate loop, no temporary list.
