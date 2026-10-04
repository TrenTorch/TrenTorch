import numpy as np

def solve(n, dim):
    """Implement positional encoding according to the contract."""
    pos = np.arange(n)[:, None]
    d = np.arange(dim)[None, :]
    rates = 1 / np.power(10000, 2 * (d // 2) / dim)
    out = pos * rates
    E = np.empty((n, dim))
    E[:, 0::2] = np.sin(out[:, 0::2])
    E[:, 1::2] = np.cos(out[:, 1::2])
    return E
