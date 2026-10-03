import numpy as np


def additive_attention(query, keys, W_q, W_k, v):
    scores = np.tanh(query @ W_q + keys @ W_k) @ v
    scores = scores - scores.max()
    w = np.exp(scores)
    w = w / w.sum()
    return w @ keys, w
