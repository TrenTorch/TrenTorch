import numpy as np

def solve(A, steps=100):
    A = np.asarray(A, dtype=float)
    v = np.ones(A.shape[0], dtype=float)
    for _ in range(steps):
        v = A @ v
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        v = v / norm
    return v
