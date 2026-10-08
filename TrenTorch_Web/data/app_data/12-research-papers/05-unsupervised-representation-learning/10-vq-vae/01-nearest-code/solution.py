import numpy as np


def nearest_code_index(z, codebook):
    d = np.linalg.norm(np.asarray(codebook, dtype=float) - np.asarray(z, dtype=float), axis=1)
    return int(np.argmin(d))
