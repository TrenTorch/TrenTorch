import numpy as np

def solve(n_features, m, seed=0):
    """Implement random feature subset according to the contract."""
    rng = np.random.default_rng(seed)
    return rng.choice(n_features, size=m, replace=False)
