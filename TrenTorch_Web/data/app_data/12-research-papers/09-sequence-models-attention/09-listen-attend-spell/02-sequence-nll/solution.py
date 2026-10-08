import numpy as np


def char_nll(logp, targets):
    logp = np.asarray(logp, dtype=float)
    targets = np.asarray(targets)
    return float(-np.sum(logp[np.arange(len(targets)), targets]))
