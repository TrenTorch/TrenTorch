import numpy as np


def byol_loss(p, z):
    p = np.asarray(p, dtype=float)
    z = np.asarray(z, dtype=float)
    cos = (p @ z) / (np.linalg.norm(p) * np.linalg.norm(z))
    return float(2 - 2 * cos)
