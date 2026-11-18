import numpy as np


def max_pool_switches(x, size):
    x = np.asarray(x, dtype=float).reshape(-1, size)
    return np.argmax(x, axis=1).astype(int)
