import numpy as np

def solve(intra, nearest):
    """Implement silhouette score one point according to the contract."""
    a = float(np.mean(intra))
    b = float(np.min(nearest))
    return 0.0 if max(a, b) == 0 else (b - a) / max(a, b)
