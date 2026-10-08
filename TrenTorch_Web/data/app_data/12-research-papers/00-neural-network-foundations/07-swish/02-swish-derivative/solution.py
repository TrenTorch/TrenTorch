import numpy as np


def swish_derivative(x, beta=1.0):
    x = np.asarray(x, dtype=float)
    s = 1.0 / (1.0 + np.exp(-beta * x))
    return s + beta * x * s * (1.0 - s)
