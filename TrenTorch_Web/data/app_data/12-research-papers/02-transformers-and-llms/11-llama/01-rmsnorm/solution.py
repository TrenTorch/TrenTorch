import numpy as np


def rmsnorm(x, g, eps=1e-6):
    x = np.asarray(x, dtype=float)
    rms = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + eps)
    return x / rms * g
