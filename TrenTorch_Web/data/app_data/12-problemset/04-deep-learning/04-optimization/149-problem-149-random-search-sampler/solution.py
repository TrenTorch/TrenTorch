import numpy as np

def solve(n, seed=0):
    """Random search samples lr logarithmically between 1e-5 and 1e-1 and an integer depth in [2,10), with repeatable draws from seed."""
    rng=np.random.default_rng(seed); return [{"lr":float(10**rng.uniform(-5,-1)),"depth":int(rng.integers(2,10))} for _ in range(n)]
