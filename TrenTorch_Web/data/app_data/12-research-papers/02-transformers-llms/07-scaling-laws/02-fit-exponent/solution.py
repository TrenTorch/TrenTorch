import numpy as np


def fit_power_law_exponent(N, L):
    slope = np.polyfit(np.log(np.asarray(N, dtype=float)), np.log(np.asarray(L, dtype=float)), 1)[0]
    return float(-slope)
