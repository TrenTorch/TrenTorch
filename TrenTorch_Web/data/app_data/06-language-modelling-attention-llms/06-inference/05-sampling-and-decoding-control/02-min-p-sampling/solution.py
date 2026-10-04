import numpy as np


def min_p_filter(probs, min_p):
    probs = np.asarray(probs, dtype=float)
    keep = probs >= min_p * probs.max()
    out = np.where(keep, probs, 0.0)
    return out / out.sum()
