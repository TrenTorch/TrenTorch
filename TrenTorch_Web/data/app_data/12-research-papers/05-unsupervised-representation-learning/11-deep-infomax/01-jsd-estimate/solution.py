import numpy as np


def jsd_estimate(pos, neg):
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    return float(np.mean(-np.logaddexp(0.0, -pos)) - np.mean(np.logaddexp(0.0, neg)))
