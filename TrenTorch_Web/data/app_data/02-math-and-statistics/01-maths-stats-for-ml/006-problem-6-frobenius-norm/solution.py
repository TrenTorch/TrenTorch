import numpy as np

def solve(A):
    A = np.asarray(A, dtype=float)
    return float(np.linalg.norm(A, ord="fro"))
