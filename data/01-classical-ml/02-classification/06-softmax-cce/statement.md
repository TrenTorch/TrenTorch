Implement:

```python
def softmax(Z: np.ndarray) -> np.ndarray:
    """Z: shape (n_samples, n_classes). Rows sum to 1."""

def cce_loss(P: np.ndarray, y_indices: np.ndarray) -> float:
    """P: shape (n_samples, n_classes) from softmax. y_indices: integer class index per sample."""
```
