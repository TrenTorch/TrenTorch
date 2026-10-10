import numpy as np

def solve(x, A, B):
    return np.asarray(B) @ (np.asarray(A) @ np.asarray(x))
