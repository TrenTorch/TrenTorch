import numpy as np

def solve(cache, new_value):
    """Implement kv cache append according to the contract."""
    return np.concatenate([cache, new_value[None, ...]], axis=-2)
