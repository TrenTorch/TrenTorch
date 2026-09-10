Implement:

```python
def train_linear_regression_production(
    X: np.ndarray,
    y: np.ndarray,
    lr: float,
    epochs: int,
    batch_size: int,
    seed: int | None = None
) -> tuple[np.ndarray, float]:
    """
    Mini-batch gradient descent, reusing linear_forward / mse_grad / gd_step
    per batch instead of once per epoch over the full dataset.
    """
```

Your function should:

1. Shuffle the sample order at the start of every epoch (a different shuffle each epoch — this is what keeps mini-batch gradients from being biased by data order).
2. Split the shuffled data into batches of `batch_size` (the last batch may be smaller if `n_samples` doesn't divide evenly — must not crash or silently drop it).
3. Take one gradient step per batch, not per epoch.
4. Never materialize more than one batch's worth of `X` at a time inside the per-batch step (no operation should touch the full `X` array once batching starts).
5. Accept an optional `seed`: when given, two calls with the same `seed` (and the same everything else) must return exactly the same `w, b` — including across epochs, not just within the first one. When `seed` is `None`, training is genuinely random run to run.
