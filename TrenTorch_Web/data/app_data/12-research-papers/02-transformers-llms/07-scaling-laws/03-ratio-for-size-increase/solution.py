import numpy as np


def loss_ratio_for_size_increase(factor, alpha):
    return np.asarray(factor, dtype=float) ** (-alpha)
