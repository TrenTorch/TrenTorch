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
