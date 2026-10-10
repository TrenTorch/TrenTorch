import numpy as np

def solve(grads):
    return np.mean(np.asarray(grads, dtype=float), axis=0)
