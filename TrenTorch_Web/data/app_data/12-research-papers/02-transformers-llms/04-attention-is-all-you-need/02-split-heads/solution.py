import numpy as np


def split_heads(x, h):
    T, d = x.shape
    return x.reshape(T, h, d // h).transpose(1, 0, 2)
