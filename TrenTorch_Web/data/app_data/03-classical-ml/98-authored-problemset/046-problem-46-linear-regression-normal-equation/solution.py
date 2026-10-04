import numpy as np

def solve(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    design = np.column_stack((np.ones(len(X)), X))
    return np.linalg.pinv(design.T @ design) @ design.T @ y
