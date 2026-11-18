import numpy as np


def residual_forward(x, f):
    return np.asarray(x, dtype=float) + f(x)
