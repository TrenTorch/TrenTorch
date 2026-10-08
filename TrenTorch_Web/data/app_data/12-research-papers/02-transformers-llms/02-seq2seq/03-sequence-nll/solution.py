import numpy as np


def sequence_nll(probs, targets):
    probs = np.asarray(probs, dtype=float)
    targets = np.asarray(targets)
    return float(-np.sum(np.log(probs[np.arange(len(targets)), targets])))
