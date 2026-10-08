import numpy as np


def symmetric_byol_loss(p1, z2, p2, z1):
    def one(p, z):
        p = np.asarray(p, dtype=float)
        z = np.asarray(z, dtype=float)
        return 2 - 2 * (p @ z) / (np.linalg.norm(p) * np.linalg.norm(z))

    return float(one(p1, z2) + one(p2, z1))
