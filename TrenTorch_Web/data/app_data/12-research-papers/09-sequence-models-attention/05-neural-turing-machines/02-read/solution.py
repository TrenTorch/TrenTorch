import numpy as np


def ntm_read(w, memory):
    return np.asarray(w, dtype=float) @ np.asarray(memory, dtype=float)
