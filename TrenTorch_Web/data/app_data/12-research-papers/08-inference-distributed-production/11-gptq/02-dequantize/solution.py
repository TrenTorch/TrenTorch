import numpy as np


def dequantize(q, scale):
    return np.asarray(q, dtype=float) * scale
