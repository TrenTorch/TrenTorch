import numpy as np

def solve(n, seed=0):
    """Implement random search sampler according to the contract."""
    rng = np.random.default_rng(seed)
    return [{'lr': float(10 ** rng.uniform(-5, -1)), 'depth': int(rng.integers(2, 10))} for _ in range(n)]
