Implement:

```python
def ridge_grad(
    X: np.ndarray,
    y_hat: np.ndarray,
    y: np.ndarray,
    w: np.ndarray,
    lam: float
) -> tuple[np.ndarray, float]:
    """
    Compute the gradient of the MSE loss with L2 regularization.
    """
```

Your function should:

1. Compute the base MSE gradient using the same formula as the earlier gradient question.
2. Extend just the _weight_ gradient with the additional penalty term derived in Theory — one that grows with both the weight's own magnitude and `lam`.
3. Leave the bias gradient untouched — bias is never regularized.
