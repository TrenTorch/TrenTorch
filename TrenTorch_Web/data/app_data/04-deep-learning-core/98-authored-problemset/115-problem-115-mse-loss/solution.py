import numpy as np

def solve(y, pred):
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.mean((y - pred) ** 2))
