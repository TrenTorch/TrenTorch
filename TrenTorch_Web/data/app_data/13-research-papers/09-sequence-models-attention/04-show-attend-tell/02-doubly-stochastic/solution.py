import numpy as np


def doubly_stochastic_penalty(alpha):
    alpha = np.asarray(alpha, dtype=float)
    return float(np.sum((1.0 - alpha.sum(axis=0)) ** 2))
