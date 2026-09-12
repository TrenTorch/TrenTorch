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
    weight: np.ndarray,
    bias: np.ndarray | None,
    grad_weight: np.ndarray,
    grad_bias: np.ndarray | None,
    lr: float,
) -> tuple[np.ndarray, np.ndarray | None]:
    """
    Apply one gradient-descent update.

    Returns:
        updated_weight, updated_bias
    """
```

Your function should:

1. Move `weight` and `bias` a step in the direction that reduces loss, scaled by `lr`, using the update rule from Theory.
2. Return new values rather than mutating the input arrays in place.
3. If `bias` is `None` (no bias parameter, matching `01-hypothesis-function` and `03-mse-gradient`), return `None` for `updated_bias` too, there is nothing to step.

## Theory

`03-mse-gradient` told us the direction in which the loss increases.

To reduce the loss, we move in the opposite direction. This is gradient descent:

```text
weight = weight - lr * grad_weight
bias   = bias   - lr * grad_bias
```

where `lr` is the learning rate. It controls how large a step we take:

- too small → learning is very slow;
- too large → we may overshoot or become unstable.

One update gives us one step toward better parameters. `weight`/`grad_weight` and `bias`/`grad_bias` are updated by the exact same rule, whatever their shape, `weight - lr * grad_weight` doesn't care whether `weight` is a scalar, a vector, or a matrix. Only `bias`'s optionality needs an explicit branch: `None` has no gradient to step against, so it stays `None`.

So the complete idea so far is:

```text
1. Make predictions        (01-hypothesis-function)
2. Calculate loss           (02-mse-loss)
3. Calculate gradients      (03-mse-gradient)
4. Update parameters        (this question)
```

## Explanation

Returns `weight - lr * grad_weight`, never `weight -= lr * grad_weight`. The in-place version mutates the caller's original array, NumPy arrays are passed by reference, so `-=` would silently corrupt anything else still holding that same `weight`, which is exactly what the "does not mutate in place" test is there to catch.

`updated_bias` is computed the same way only when `bias` is not `None`. There's no `grad_bias` to apply when there was never a `bias` parameter to begin with, and returning a fabricated zero-stepped bias would silently invent a parameter that doesn't exist.
