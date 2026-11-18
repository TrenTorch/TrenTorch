import numpy as np


def l2_normalize(z):
    z = np.asarray(z, dtype=float)
    n = np.linalg.norm(z)
    if n == 0:
        return np.zeros_like(z)
    return z / n
