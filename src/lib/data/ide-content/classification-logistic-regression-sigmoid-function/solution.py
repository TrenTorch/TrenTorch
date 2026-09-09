import numpy as np


def sigmoid(x):
    """Elementwise sigmoid: 1 / (1 + exp(-x))."""
    return 1.0 / (1.0 + np.exp(-x))
