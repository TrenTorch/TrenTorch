import numpy as np

def solve(fan_in, fan_out, seed=0):
    rng = np.random.default_rng(seed)
    bound = np.sqrt(6.0 / (fan_in + fan_out))
    return rng.uniform(-bound, bound, size=(fan_in, fan_out))
