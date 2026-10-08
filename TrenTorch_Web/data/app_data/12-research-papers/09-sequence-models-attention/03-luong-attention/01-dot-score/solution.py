import numpy as np


def dot_score(h_t, h_s):
    return float(np.asarray(h_t, dtype=float) @ np.asarray(h_s, dtype=float))
