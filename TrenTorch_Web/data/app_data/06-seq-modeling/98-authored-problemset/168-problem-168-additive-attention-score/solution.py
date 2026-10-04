import numpy as np

def solve(Q, K, Wq, Wk):
    """Implement additive attention score according to the contract."""
    return np.tanh(np.asarray(Q) @ Wq + np.asarray(K) @ Wk).sum(-1)
