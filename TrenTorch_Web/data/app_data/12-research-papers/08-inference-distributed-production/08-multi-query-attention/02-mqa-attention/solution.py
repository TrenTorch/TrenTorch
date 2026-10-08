import numpy as np


def multi_query_attention(q, k, v):
    d = q.shape[-1]
    scores = q @ k.T / np.sqrt(d)
    e = np.exp(scores - scores.max(axis=-1, keepdims=True))
    w = e / e.sum(axis=-1, keepdims=True)
    return w @ v
