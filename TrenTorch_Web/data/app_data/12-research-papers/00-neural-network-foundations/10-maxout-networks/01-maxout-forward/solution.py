import numpy as np


def maxout_forward(x, W, b, k):
    z = x @ W.T + b
    z = z.reshape(z.shape[0], -1, k)
    return z.max(axis=-1)
