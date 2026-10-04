import numpy as np

def solve(rewards):
    """Implement rlhf reward normalization according to the contract."""
    r = np.asarray(rewards, float)
    return (r - r.mean()) / r.std()
