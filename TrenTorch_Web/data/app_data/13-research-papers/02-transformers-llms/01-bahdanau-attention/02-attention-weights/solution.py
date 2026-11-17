import numpy as np


def attention_weights(scores):
    scores = np.asarray(scores, dtype=float)
    e = np.exp(scores - scores.max())
    return e / e.sum()
