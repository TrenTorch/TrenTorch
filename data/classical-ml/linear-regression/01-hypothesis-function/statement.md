Implement:

```python
def linear_forward(
    X: np.ndarray,
    w: np.ndarray,
    b: float
) -> np.ndarray:
    """
    X: shape (n_samples, n_features)
    w: shape (n_features,)
    b: scalar

    Returns:
        Predictions with shape (n_samples,)
    """
```

Your function should:

1. Return exactly one prediction per sample, using the rule derived in Theory.
2. Support any number of features, including exactly one.
3. Compute all samples in a single vectorized expression — no Python `for` loop over samples.
4. Preserve `X`'s dtype in the output (don't hardcode `float32`/`float64`).
