import numpy as np

def solve(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    variance_a = np.var(a, ddof=1)
    variance_b = np.var(b, ddof=1)
    return float((a.mean() - b.mean()) / np.sqrt(variance_a / len(a) + variance_b / len(b)))
