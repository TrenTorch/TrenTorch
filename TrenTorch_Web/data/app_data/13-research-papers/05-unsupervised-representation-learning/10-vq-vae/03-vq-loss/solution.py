import numpy as np


def vq_loss(z, e, beta):
    z = np.asarray(z, dtype=float)
    e = np.asarray(e, dtype=float)
    return float(np.mean((z - e) ** 2) * (1 + beta))
