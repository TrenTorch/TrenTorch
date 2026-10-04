import numpy as np

def solve(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    pooled = (a.sum() + b.sum()) / (len(a) + len(b))
    se = np.sqrt(pooled * (1 - pooled) * (1 / len(a) + 1 / len(b)))
    return float((a.mean() - b.mean()) / se)
