import numpy as np


def probability_ratio(logp_new, logp_old):
    return np.exp(np.asarray(logp_new, dtype=float) - np.asarray(logp_old, dtype=float))
