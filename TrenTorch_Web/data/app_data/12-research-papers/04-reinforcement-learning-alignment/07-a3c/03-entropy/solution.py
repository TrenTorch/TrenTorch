import numpy as np


def entropy(p):
    p = np.asarray(p, dtype=float)
    safe = np.where(p > 0, p, 1.0)
    return float(-np.sum(np.where(p > 0, p * np.log(safe), 0.0)))
