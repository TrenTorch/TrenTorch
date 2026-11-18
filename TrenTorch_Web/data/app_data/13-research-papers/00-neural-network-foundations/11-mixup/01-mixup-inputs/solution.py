import numpy as np


def mixup_inputs(x, perm, lam):
    x = np.asarray(x, dtype=float)
    return lam * x + (1 - lam) * x[perm]
