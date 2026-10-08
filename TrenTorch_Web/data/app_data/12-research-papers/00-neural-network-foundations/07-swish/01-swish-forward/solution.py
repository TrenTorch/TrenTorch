import numpy as np


def swish(x, beta=1.0):
    x = np.asarray(x, dtype=float)
    return x / (1.0 + np.exp(-beta * x))
