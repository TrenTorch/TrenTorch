import numpy as np


def scaled_dot_product_attention(Q, K, V):
    d = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d)
    e = np.exp(scores - scores.max(axis=-1, keepdims=True))
    w = e / e.sum(axis=-1, keepdims=True)
    return w @ V
