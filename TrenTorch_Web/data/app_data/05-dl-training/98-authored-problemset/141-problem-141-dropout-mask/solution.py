import numpy as np

def solve(x, keep_prob, seed=0):
    """Implement dropout mask according to the contract."""
    rng = np.random.default_rng(seed)
    mask = rng.random(np.asarray(x).shape) < keep_prob
    return np.asarray(x) * mask / keep_prob
