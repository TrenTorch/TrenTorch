import numpy as np


def cross_attention(x_dec, enc, W_q, W_k, W_v, enc_mask):
    Q, K, V = x_dec @ W_q, enc @ W_k, enc @ W_v
    scores = Q @ K.T / np.sqrt(Q.shape[1])
    scores = np.where(np.asarray(enc_mask)[None, :] == 1, scores, -np.inf)
    scores = scores - scores.max(axis=1, keepdims=True)
    w = np.exp(scores)
    w = w / w.sum(axis=1, keepdims=True)
    return w @ V, w
