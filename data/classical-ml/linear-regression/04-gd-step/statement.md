Implement:

```python
def gd_step(
    w: np.ndarray,
    b: float,
    dw: np.ndarray,
    db: float,
    lr: float
) -> tuple[np.ndarray, float]:
    """
    Apply one gradient-descent update.

    Returns:
        updated_w, updated_b
    """
```

Your function should:

1. Move `w` and `b` a step in the direction that reduces loss, scaled by `lr`, using the update rule from Theory.
2. Return new values rather than mutating the input arrays in place.
