Implement:

```python
def train_logistic_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    """
    Returns final_w, final_b.
    """
```

Reuse `sigmoid` and `bce_grad` rather than reimplementing their logic.
