import numpy as np


def highway_gate(x, W, b):
    z = x @ W.T + b
    return 1.0 / (1.0 + np.exp(-z))
