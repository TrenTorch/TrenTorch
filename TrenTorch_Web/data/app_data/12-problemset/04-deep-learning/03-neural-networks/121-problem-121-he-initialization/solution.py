import numpy as np

def solve(fan_in, fan_out, seed=0):
    rng = np.random.default_rng(seed)
    std = np.sqrt(2.0 / fan_in)
    return rng.normal(0.0, std, size=(fan_in, fan_out))
