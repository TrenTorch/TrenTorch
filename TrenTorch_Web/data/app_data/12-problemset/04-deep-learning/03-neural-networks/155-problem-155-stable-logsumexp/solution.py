import numpy as np

def solve(x):
    """Compute log(sum(exp(x))) stably for a non-empty one-dimensional input."""
    values = np.asarray(x, dtype=float)
    if values.size == 0:
        raise ValueError("x must not be empty")
    maximum = np.max(values)
    return float(maximum + np.log(np.exp(values - maximum).sum()))
