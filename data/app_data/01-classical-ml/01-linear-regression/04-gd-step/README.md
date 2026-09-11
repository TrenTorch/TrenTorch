---
name: linear-regression-gd-step
title: One Gradient-Descent Update
tags: [classical-ml, linear-regression, gradient-descent, optimization]
difficulty: Beginner
---

## Statement

Implement:

```python
def gd_step(
    w: np.ndarray,
    b: float,
    dw: np.ndarray,
    db: float,
    lr: float
) -> tuple[np.ndarray, float]:
    """
    Apply one gradient-descent update.

    Returns:
        updated_w, updated_b
    """
```

Your function should:

1. Move `w` and `b` a step in the direction that reduces loss, scaled by `lr`, using the update rule from Theory.
2. Return new values rather than mutating the input arrays in place.

## Theory

We now know the direction in which the loss increases.

To reduce the loss, we move in the opposite direction.

This is gradient descent:

```text
w = w - lr * dw
b = b - lr * db
```

where `lr` is the learning rate.

The learning rate controls how large a step we take:

- too small → learning is very slow;
- too large → we may overshoot or become unstable.

One update gives us one step toward better parameters.

So the complete idea so far is:

```text
1. Make predictions
2. Calculate loss
3. Calculate gradients
4. Update parameters
```

## Explanation

Returns `w - lr * dw`, never `w -= lr * dw`. The in-place version mutates the caller's original array — NumPy arrays are passed by reference, so `-=` would silently corrupt anything else still holding that same `w`, which is exactly what the "does not mutate in place" test is there to catch.
