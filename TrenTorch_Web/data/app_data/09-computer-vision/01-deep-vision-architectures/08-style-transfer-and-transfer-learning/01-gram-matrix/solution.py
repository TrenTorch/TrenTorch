import numpy as np


def gram_matrix(features):
    C = features.shape[0]
    F = np.asarray(features, dtype=float).reshape(C, -1)
    return F @ F.T / F.size
