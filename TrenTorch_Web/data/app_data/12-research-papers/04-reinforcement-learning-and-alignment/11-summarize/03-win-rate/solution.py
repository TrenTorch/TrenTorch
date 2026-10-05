import numpy as np


def win_rate(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.mean(a > b) + 0.5 * np.mean(a == b))
