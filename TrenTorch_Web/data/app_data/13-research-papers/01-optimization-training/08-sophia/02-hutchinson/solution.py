import numpy as np


def hutchinson_estimate(Hu, u):
    return np.asarray(Hu, dtype=float) * np.asarray(u, dtype=float)
