import numpy as np

def solve(lengths):
    """Return exclusive cumulative offsets for concatenated variable-length rows."""
    lengths = np.asarray(lengths, dtype=int)
    if np.any(lengths < 0):
        raise ValueError("lengths must be non-negative")
    return np.cumsum(lengths) - lengths
