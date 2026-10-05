import numpy as np

def solve(A, x):
    A = np.asarray(A, dtype=float)
    x = np.asarray(x, dtype=float)
    return A @ x
