import numpy as np


def weight_norm_linear(x, v, g, b):
    v = np.asarray(v, dtype=float)
    norms = np.sqrt(np.sum(v**2, axis=1, keepdims=True))
    W = g[:, None] * v / norms
    return x @ W.T + b
