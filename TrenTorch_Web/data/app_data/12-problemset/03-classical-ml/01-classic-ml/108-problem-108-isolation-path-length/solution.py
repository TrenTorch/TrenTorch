import numpy as np

def solve(x, lo, hi, max_depth, rng):
    """A randomized isolation path repeatedly splits the current interval; the returned path length is the number of splits before the depth cap."""
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
