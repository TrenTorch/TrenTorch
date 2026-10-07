import numpy as np

def solve(y, p, bins=10):
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    if y.shape != p.shape or y.ndim != 1:
        raise ValueError("y and p must be 1-D and the same length")
    if not np.all((y == 0) | (y == 1)):
        raise ValueError("y must contain only 0/1 labels")
    if np.any(p < 0) or np.any(p > 1):
        raise ValueError("p must lie in [0, 1]")
    edges = np.linspace(0.0, 1.0, bins + 1)
    out = []
    for i in range(bins):
        in_bin = (p >= edges[i]) & ((p < edges[i + 1]) if i < bins - 1 else (p <= edges[i + 1]))
        if np.any(in_bin):
            out.append((float(p[in_bin].mean()), float(y[in_bin].mean()), int(in_bin.sum())))
    return out
