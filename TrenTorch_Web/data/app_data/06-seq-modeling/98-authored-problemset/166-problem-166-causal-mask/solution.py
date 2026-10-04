import numpy as np

def solve(n):
    """Return an n-by-n boolean causal mask allowing keys at or before each query."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return np.tril(np.ones((n, n), dtype=bool))
