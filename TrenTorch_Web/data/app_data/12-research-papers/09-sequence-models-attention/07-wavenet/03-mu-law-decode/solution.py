import numpy as np


def mu_law_decode(y, mu=255):
    y = np.asarray(y, dtype=float)
    return np.sign(y) * ((1 + mu) ** np.abs(y) - 1) / mu
