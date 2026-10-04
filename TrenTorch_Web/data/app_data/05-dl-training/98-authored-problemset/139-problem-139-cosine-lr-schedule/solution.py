import numpy as np

def solve(lr_max, lr_min, t, T):
    """Implement cosine lr schedule according to the contract."""
    if T <= 0:
        return float(lr_min)
    q = min(max(t, 0), T)
    return float(lr_min + 0.5 * (lr_max - lr_min) * (1 + np.cos(np.pi * q / T)))
