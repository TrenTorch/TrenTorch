import numpy as np


def softplus(x):
    return np.logaddexp(0.0, np.asarray(x, dtype=float))
