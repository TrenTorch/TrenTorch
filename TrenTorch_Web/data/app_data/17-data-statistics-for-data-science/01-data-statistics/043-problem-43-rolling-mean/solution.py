import numpy as np

def solve(x, window):
    """Implement rolling mean according to the contract."""
    x = np.asarray(x, float)
    out = np.full(len(x), np.nan)
    s = 0.0
    for i, v in enumerate(x):
        s += v
        if i >= window:
            s -= x[i - window]
        if i >= window - 1:
            out[i] = s / window
    return out
