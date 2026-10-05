import numpy as np

def solve(y, p, bins=10):
    y = np.asarray(y)
    p = np.asarray(p)
    edges = np.linspace(0.0, 1.0, bins + 1)
    result = []
    for i in range(bins):
        in_bin = (p >= edges[i]) & (p < edges[i + 1] if i < bins - 1 else p <= edges[i + 1])
        if np.any(in_bin):
            result.append((float(p[in_bin].mean()), float(y[in_bin].mean()), int(in_bin.sum())))
    return result
