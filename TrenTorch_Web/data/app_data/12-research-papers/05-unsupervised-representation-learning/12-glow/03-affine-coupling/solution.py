import numpy as np


def affine_coupling_forward(xa, xb, s, t):
    xa = np.asarray(xa, dtype=float)
    xb = np.asarray(xb, dtype=float)
    return xa, xb * np.exp(s) + t
