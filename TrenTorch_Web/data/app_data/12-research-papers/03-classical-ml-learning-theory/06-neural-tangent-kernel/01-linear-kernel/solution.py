import numpy as np


def linear_kernel_matrix(X1, X2):
    return np.asarray(X1, dtype=float) @ np.asarray(X2, dtype=float).T
