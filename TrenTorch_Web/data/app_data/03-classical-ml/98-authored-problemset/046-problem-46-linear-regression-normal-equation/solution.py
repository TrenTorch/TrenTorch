import numpy as np

def solve(X, y):
    """Implement linear regression normal equation according to the contract."""
    X, y = (np.asarray(X, float), np.asarray(y, float))
    A = np.c_[np.ones(len(X)), X]
    return np.linalg.pinv(A.T @ A) @ A.T @ y
