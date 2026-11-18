import numpy as np


def memory_match(u, M):
    return np.asarray(M, dtype=float) @ np.asarray(u, dtype=float)
