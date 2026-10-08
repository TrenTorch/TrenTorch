import numpy as np


def nonrecurrent_dropout(h, mask, p):
    return np.asarray(h, dtype=float) * mask / (1 - p)
