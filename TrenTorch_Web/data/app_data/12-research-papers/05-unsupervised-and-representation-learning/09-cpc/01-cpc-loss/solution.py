import numpy as np


def cpc_loss(scores, pos):
    scores = np.asarray(scores, dtype=float)
    return float(np.logaddexp.reduce(scores) - scores[pos])
