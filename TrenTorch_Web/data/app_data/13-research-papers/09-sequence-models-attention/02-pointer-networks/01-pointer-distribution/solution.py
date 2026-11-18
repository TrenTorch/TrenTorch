import numpy as np


def pointer_distribution(scores):
    scores = np.asarray(scores, dtype=float)
    e = np.exp(scores - scores.max())
    return e / e.sum()
