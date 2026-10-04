import numpy as np

def solve(query, keys, Wq, Wk, v):
    """Return additive-attention scores for one query against all key vectors."""
    hidden = np.tanh(np.asarray(query) @ Wq + np.asarray(keys) @ Wk)
    return hidden @ np.asarray(v)
