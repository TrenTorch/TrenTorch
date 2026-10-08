import numpy as np


def highway_layer(x, W_h, b_h, W_t, b_t):
    h = np.tanh(x @ W_h.T + b_h)
    t = 1.0 / (1.0 + np.exp(-(x @ W_t.T + b_t)))
    return h * t + x * (1 - t)
