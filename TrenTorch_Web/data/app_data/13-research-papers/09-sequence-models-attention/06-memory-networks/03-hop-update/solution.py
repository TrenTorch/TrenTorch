import numpy as np


def hop_update(u, o):
    return np.asarray(u, dtype=float) + np.asarray(o, dtype=float)
