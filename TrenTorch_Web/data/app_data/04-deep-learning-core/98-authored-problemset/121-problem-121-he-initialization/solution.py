import numpy as np

def solve(fan_in, fan_out, seed=0):
    """Implement he initialization according to the contract."""
    rng = np.random.default_rng(seed)
    return rng.normal(0, np.sqrt(2 / fan_in), (fan_in, fan_out))
