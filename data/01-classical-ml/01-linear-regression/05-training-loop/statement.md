Implement:

```python
def train_linear_regression(
    X: np.ndarray,
    y: np.ndarray,
    lr: float,
    epochs: int
) -> tuple[np.ndarray, float]:
    """
    Train a linear regression model using gradient descent.

    Returns:
        final_w, final_b
    """
```

Your function should:

1. Initialize `w` and `b` to zero values.
2. Repeat the following for `epochs` iterations:
   - call `linear_forward()` to calculate predictions;
   - call `mse_grad()` to calculate `dw` and `db`;
   - call `gd_step()` to update `w` and `b`.
3. Return the final `w` and `b`.

Use the functions you already implemented in the earlier questions rather than reimplementing their logic inside the training loop.
