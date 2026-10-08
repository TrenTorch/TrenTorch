import numpy as np


def sinusoidal_positional_encoding(T, d):
    pos = np.arange(T)[:, None]
    i = np.arange(d // 2)[None, :]
    angles = pos / (10000.0 ** (2 * i / d))
    pe = np.zeros((T, d))
    pe[:, 0::2] = np.sin(angles)
    pe[:, 1::2] = np.cos(angles)
    return pe
