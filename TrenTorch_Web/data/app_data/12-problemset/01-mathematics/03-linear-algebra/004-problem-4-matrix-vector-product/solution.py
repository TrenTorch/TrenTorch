import numpy as np

def solve(A, x):
        A, x = np.asarray(A, float), np.asarray(x, float)
        return np.array([row @ x for row in A])
