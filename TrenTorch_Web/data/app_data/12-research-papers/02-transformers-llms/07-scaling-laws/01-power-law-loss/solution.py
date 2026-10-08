import numpy as np


def power_law_loss(N, N_c, alpha):
    return (np.asarray(N_c, dtype=float) / np.asarray(N, dtype=float)) ** alpha
