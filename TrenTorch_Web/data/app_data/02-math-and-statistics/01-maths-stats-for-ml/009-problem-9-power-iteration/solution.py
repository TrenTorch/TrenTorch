import numpy as np

def solve(A, steps=100):
    """Implement power iteration according to the contract."""
    A = np.asarray(A, float)
    v = np.ones(A.shape[0])
    for _ in range(steps):
        v = A @ v
        n = np.linalg.norm(v)
        if n == 0:
            return v
        v = v / n
    return v
