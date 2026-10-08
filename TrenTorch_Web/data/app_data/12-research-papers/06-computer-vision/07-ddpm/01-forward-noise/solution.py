import numpy as np


def forward_noise(x0, ab, eps):
    return np.sqrt(ab) * np.asarray(x0, dtype=float) + np.sqrt(1 - ab) * np.asarray(eps, dtype=float)
