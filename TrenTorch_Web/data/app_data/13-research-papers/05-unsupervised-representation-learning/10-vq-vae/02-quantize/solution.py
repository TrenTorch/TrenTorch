import numpy as np


def quantize(codebook, idx):
    return np.asarray(codebook, dtype=float)[idx]
