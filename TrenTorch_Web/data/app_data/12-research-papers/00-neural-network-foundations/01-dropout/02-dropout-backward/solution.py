import numpy as np


def dropout_backward(grad_out, keep_mask, p):
    return np.asarray(grad_out, dtype=float) * keep_mask / (1 - p)
