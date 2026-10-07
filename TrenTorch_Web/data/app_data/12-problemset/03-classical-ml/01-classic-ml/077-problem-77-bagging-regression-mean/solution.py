import numpy as np

def solve(predictions):
    return np.asarray(predictions, dtype=float).mean(axis=0)
