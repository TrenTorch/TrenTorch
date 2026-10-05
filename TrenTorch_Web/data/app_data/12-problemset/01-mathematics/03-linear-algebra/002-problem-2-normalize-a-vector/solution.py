import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    norm = np.linalg.norm(x)
    if norm == 0:
        raise ValueError("cannot normalize the zero vector")
    return x / norm
