import numpy as np


def actnorm_forward(x, scale, bias):
    return (np.asarray(x, dtype=float) + bias) * scale
