import numpy as np

def solve(n, dim):
    """Construct the standard alternating sine/cosine positional encoding."""
    if n < 0 or dim <= 0:
        raise ValueError("n must be non-negative and dim must be positive")
    positions = np.arange(n)[:, None]
    dimensions = np.arange(dim)[None, :]
    rates = 1 / np.power(10000, (2 * (dimensions // 2)) / dim)
    angles = positions * rates
    encoding = np.empty((n, dim), dtype=float)
    encoding[:, 0::2] = np.sin(angles[:, 0::2])
    encoding[:, 1::2] = np.cos(angles[:, 1::2])
    return encoding
