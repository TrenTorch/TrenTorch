import numpy as np


def recalibrate(x, s):
    return np.asarray(x, dtype=float) * np.asarray(s, dtype=float)
