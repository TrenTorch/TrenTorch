import numpy as np

def solve(query, keys, Wq, Wk, v):
    hidden = np.tanh(np.asarray(query) @ Wq + np.asarray(keys) @ Wk)
    return hidden @ np.asarray(v)
