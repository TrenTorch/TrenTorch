import numpy as np


def gelu_tanh(x):
    x = np.asarray(x, dtype=float)
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))
