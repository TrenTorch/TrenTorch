import numpy as np


def swiglu(x, W, V):
    z = x @ W
    silu = z / (1.0 + np.exp(-z))
    return silu * (x @ V)
