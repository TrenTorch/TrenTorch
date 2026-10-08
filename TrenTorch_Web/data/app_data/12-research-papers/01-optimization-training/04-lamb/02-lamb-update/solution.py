import numpy as np


def lamb_update(w, r, lr):
    ratio = np.linalg.norm(w) / np.linalg.norm(r)
    return w - lr * ratio * r
