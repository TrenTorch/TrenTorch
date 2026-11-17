import numpy as np


def sample_lambda(alpha, rng):
    return float(rng.beta(alpha, alpha))


def mixup(x1, y1, x2, y2, lam):
    return lam * np.asarray(x1) + (1 - lam) * np.asarray(x2), lam * np.asarray(y1) + (1 - lam) * np.asarray(y2)
