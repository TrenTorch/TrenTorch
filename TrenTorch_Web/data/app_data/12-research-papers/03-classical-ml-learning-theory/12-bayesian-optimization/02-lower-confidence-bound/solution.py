import numpy as np


def lower_confidence_bound(mu, sigma, kappa):
    return np.asarray(mu, dtype=float) - kappa * np.asarray(sigma, dtype=float)
