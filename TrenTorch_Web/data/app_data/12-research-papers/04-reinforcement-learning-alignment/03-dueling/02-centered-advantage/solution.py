import numpy as np


def centered_advantage(A):
    A = np.asarray(A, dtype=float)
    return A - A.mean()
