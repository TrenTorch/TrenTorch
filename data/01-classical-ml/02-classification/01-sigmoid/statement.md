Implement:

```python
def sigmoid(z: np.ndarray) -> np.ndarray:
    """
    z: any shape of real numbers.
    Returns elementwise sigmoid, same shape as z, values strictly in (0, 1).
    """
```

Your function should:

1. Work elementwise on arrays of any shape.
2. Never overflow or return `nan`, even for very large `|z|`.
3. Return exactly `0.5` when `z = 0`.
