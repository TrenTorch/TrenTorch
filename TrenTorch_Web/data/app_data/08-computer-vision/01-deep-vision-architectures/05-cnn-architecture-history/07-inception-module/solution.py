import numpy as np


def conv2d_same(x, w):
    x = np.asarray(x, dtype=float)
    O, C, k, _ = w.shape
    _, H, W = x.shape
    r = k // 2
    xp = np.pad(x, ((0, 0), (r, r), (r, r)))
    out = np.zeros((O, H, W))
    for i in range(k):
        for j in range(k):
            out += np.einsum("oc,chw->ohw", w[:, :, i, j], xp[:, i:i + H, j:j + W])
    return out


def _relu(a):
    return np.maximum(a, 0.0)


def _maxpool3_same(x):
    C, H, W = x.shape
    xp = np.pad(x, ((0, 0), (1, 1), (1, 1)), constant_values=-np.inf)
    return np.max([xp[:, i:i + H, j:j + W] for i in range(3) for j in range(3)], axis=0)


def inception_forward(x, p):
    b1 = _relu(conv2d_same(x, p["b1"]))
    b2 = _relu(conv2d_same(_relu(conv2d_same(x, p["b2a"])), p["b2b"]))
    b3 = _relu(conv2d_same(_relu(conv2d_same(x, p["b3a"])), p["b3b"]))
    b4 = _relu(conv2d_same(_maxpool3_same(np.asarray(x, dtype=float)), p["b4"]))
    return np.concatenate([b1, b2, b3, b4], axis=0)
