import numpy as np


def mu_law_encode(x, mu=255):
    x = np.asarray(x, dtype=float)
    return np.sign(x) * np.log1p(mu * np.abs(x)) / np.log1p(mu)
