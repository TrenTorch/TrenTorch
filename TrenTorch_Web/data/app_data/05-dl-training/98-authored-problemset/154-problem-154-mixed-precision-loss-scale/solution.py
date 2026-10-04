import numpy as np

def solve(loss, scaled_grads, scale):
    """Implement mixed precision loss scale according to the contract."""
    scaled = loss * scale
    unscaled = [np.asarray(g) / scale for g in scaled_grads]
    return (scaled, unscaled)
