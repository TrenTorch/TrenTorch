import numpy as np


def prelu(x, a):
    x = np.asarray(x, dtype=float)
    return np.where(x > 0, x, a * x)
