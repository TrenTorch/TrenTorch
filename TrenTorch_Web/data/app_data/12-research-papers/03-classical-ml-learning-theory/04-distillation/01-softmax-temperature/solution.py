import numpy as np


def softmax_temperature(logits, T):
    z = np.asarray(logits, dtype=float) / T
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)
