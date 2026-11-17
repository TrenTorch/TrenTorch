import numpy as np


def normalize_last_axis(x, eps=1e-5):
    x = np.asarray(x, dtype=float)
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)
