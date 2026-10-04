import numpy as np

def solve(w, lam):
    """Implement weight decay penalty according to the contract."""
    w = np.asarray(w, float)
    return float(lam * np.sum(w * w))
