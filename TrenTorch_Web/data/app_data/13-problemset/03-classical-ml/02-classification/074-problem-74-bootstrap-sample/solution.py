import numpy as np

def solve(n,seed=0):
        rng=np.random.default_rng(seed); return rng.integers(0,n,size=n)
