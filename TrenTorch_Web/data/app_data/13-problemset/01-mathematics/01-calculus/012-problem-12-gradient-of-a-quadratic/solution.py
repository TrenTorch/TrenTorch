import numpy as np

def solve(A, x, b):
    A = np.asarray(A, dtype=float)
    x = np.asarray(x, dtype=float)
    b = np.asarray(b, dtype=float)
    return 0.5 * (A + A.T) @ x + b
