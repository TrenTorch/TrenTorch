import numpy as np


def inverse_root(eigs, power):
    return np.asarray(eigs, dtype=float) ** (-1.0 / power)
