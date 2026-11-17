import numpy as np


def pointwise_mlp(x, layers):
    h = np.asarray(x, dtype=float)
    for idx, (W, b) in enumerate(layers):
        h = np.einsum("oc,chw->ohw", W, h) + b[:, None, None]
        if idx < len(layers) - 1:
            h = np.maximum(h, 0.0)
    return h


def global_avg_pool(x):
    return np.asarray(x, dtype=float).mean(axis=(1, 2))


def nin_logits(x, layers):
    return global_avg_pool(pointwise_mlp(x, layers))
