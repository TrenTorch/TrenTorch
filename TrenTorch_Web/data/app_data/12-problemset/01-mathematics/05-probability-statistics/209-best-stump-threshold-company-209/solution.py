import numpy as np

def solve(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=int)
    order = np.argsort(x, kind="stable")
    x = x[order]
    y = y[order]
    best = None
    for i in range(1, len(x)):
        if x[i] == x[i - 1]:
            continue
        threshold = (x[i] + x[i - 1]) / 2
        score = (i * _gini(y[:i]) + (len(y) - i) * _gini(y[i:])) / len(y)
        if best is None or score < best[0] - 1e-12:
            best = (score, threshold)
    if best is None:
        raise ValueError("need at least two distinct feature values")
    return float(best[1])

def _gini(labels):
    p = np.mean(labels == 1)
    return 1 - p * p - (1 - p) * (1 - p)
