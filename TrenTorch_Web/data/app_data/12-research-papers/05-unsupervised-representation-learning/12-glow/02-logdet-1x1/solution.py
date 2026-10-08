import numpy as np


def logdet_1x1(W, h, w):
    sign, logabsdet = np.linalg.slogdet(np.asarray(W, dtype=float))
    return float(h * w * logabsdet)
