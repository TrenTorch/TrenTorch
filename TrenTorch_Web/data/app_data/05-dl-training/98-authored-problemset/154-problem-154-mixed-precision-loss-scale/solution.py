import numpy as np

def solve(loss, scaled_grads, scale):
    """Scale the loss and unscale each gradient using the same positive scale."""
    if scale <= 0:
        raise ValueError("scale must be positive")
    return loss * scale, [np.asarray(g, dtype=float) / scale for g in scaled_grads]
