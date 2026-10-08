import numpy as np


def general_score(h_t, W, h_s):
    return float(np.asarray(h_t, dtype=float) @ np.asarray(W, dtype=float) @ np.asarray(h_s, dtype=float))
