import numpy as np

def solve(x, lo, hi, max_depth, rng):
    """Implement isolation path length according to the contract."""
    x = float(x)
    depth = 0
    lo, hi = (float(lo), float(hi))
    while depth < max_depth and lo < hi:
        split = rng.uniform(lo, hi)
        depth += 1
        if x <= split:
            hi = split
        else:
            lo = split
    return depth
