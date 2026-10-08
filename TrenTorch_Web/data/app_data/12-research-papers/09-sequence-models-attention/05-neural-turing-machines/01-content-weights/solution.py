import numpy as np


def content_weights(memory, key, beta):
    M = np.asarray(memory, dtype=float)
    k = np.asarray(key, dtype=float)
    cos = (M @ k) / (np.linalg.norm(M, axis=1) * np.linalg.norm(k) + 1e-12)
    e = np.exp(beta * (cos - cos.max()))
    return e / e.sum()
