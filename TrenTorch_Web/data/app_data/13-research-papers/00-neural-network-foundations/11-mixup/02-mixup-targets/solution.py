import numpy as np


def mixup_targets(y, perm, lam):
    y = np.asarray(y, dtype=float)
    return lam * y + (1 - lam) * y[perm]
