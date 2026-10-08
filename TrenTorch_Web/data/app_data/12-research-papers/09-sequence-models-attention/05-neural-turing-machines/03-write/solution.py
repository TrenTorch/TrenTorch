import numpy as np


def ntm_write(memory, w, erase, add):
    M = np.asarray(memory, dtype=float)
    w = np.asarray(w, dtype=float)
    return M * (1 - np.outer(w, erase)) + np.outer(w, add)
