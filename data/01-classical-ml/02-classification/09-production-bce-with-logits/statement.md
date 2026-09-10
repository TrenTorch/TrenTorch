Implement:

```python
def bce_with_logits_loss(z: np.ndarray, y: np.ndarray) -> float:
    """
    Numerically stable BCE computed directly from raw logits z,
    without ever computing a separate sigmoid(z) probability array.
    """
```

Your function should:

1. Never call `sigmoid()` or compute `exp(z)` for positive `z` anywhere in the implementation — only `exp(-|z|)`.
2. Match plain `bce_loss(sigmoid(z), y)` on ordinary, non-extreme inputs.
3. Stay finite and correct for `z` values large enough that `sigmoid(z)` itself would already round to exactly 0.0 or 1.0.
