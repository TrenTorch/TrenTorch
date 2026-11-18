import numpy as np


def dropout_forward(x, keep_mask, p):
    return np.asarray(x, dtype=float) * keep_mask / (1 - p)
