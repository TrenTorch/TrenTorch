import numpy as np

def solve(x, p, seed=0):
    if not 0 <= p < 1:
        raise ValueError("p must satisfy 0 <= p < 1")
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    mask = rng.random(x.shape) >= p
    return x * mask / (1 - p)
