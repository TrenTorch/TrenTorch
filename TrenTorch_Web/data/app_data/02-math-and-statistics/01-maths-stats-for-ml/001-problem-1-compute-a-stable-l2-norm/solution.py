import numpy as np

def solve(x):
    """Implement compute a stable l2 norm according to the contract."""
    x = np.asarray(x, dtype=float)
    scale = np.max(np.abs(x))
    if scale == 0:
        return 0.0
    return float(scale * np.sqrt(np.sum((x / scale) ** 2)))
