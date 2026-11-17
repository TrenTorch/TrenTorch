import numpy as np


def dueling_q(V, A):
    A = np.asarray(A, dtype=float)
    return V + A - A.mean()
