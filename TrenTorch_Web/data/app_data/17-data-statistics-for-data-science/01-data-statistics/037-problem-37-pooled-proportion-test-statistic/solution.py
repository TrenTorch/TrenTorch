import numpy as np

def solve(a, b):
    """Implement pooled proportion test statistic according to the contract."""
    a, b = (np.asarray(a, float), np.asarray(b, float))
    p = (a.sum() + b.sum()) / (len(a) + len(b))
    se = np.sqrt(p * (1 - p) * (1 / len(a) + 1 / len(b)))
    return float((a.mean() - b.mean()) / se)
