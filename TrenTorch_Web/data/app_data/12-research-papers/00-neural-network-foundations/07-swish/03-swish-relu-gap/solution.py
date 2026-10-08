import numpy as np


def swish_relu_gap(x, beta=1.0):
    x = np.asarray(x, dtype=float)
    swish_vals = x / (1.0 + np.exp(-beta * x))
    relu_vals = np.maximum(x, 0.0)
    return float(np.max(np.abs(swish_vals - relu_vals)))
