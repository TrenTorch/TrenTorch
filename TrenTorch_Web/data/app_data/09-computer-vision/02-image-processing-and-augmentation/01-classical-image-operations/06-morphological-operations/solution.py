import numpy as np


def _window_reduce(binary, k, fn):
    b = np.asarray(binary)
    r = k // 2
    H, W = b.shape
    padded = np.pad(b, r, mode="constant", constant_values=0)
    stack = [padded[i:i + H, j:j + W] for i in range(k) for j in range(k)]
    return fn(np.stack(stack), axis=0).astype(b.dtype)


def erode(binary, k):
    return _window_reduce(binary, k, np.min)


def dilate(binary, k):
    return _window_reduce(binary, k, np.max)


def opening(binary, k):
    return dilate(erode(binary, k), k)
