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
