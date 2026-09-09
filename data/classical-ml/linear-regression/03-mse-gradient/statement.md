Implement:

```python
def mse_grad(
    X: np.ndarray,
    y_hat: np.ndarray,
    y: np.ndarray
) -> tuple[np.ndarray, float]:
    """
    Returns:
        dw: gradient with respect to w
        db: gradient with respect to b
    """
```

Use the formulas:

```text
dw = (2/n) * X.T @ (y_hat - y)
db = (2/n) * sum(y_hat - y)
```

Do not use an autograd library.
