import numpy as np


def soft_context(alpha, feats):
    return np.asarray(alpha, dtype=float) @ np.asarray(feats, dtype=float)
