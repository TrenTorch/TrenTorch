import numpy as np


def dueling_argmax(V, A):
    A = np.asarray(A, dtype=float)
    q = V + A - A.mean()
    return int(np.argmax(q))
