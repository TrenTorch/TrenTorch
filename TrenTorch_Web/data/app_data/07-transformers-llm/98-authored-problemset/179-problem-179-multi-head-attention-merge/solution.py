import numpy as np

def solve(X):
    """Implement multi-head attention merge according to the contract."""
    X = np.asarray(X)
    B, H, T, D = X.shape
    return X.transpose(0, 2, 1, 3).reshape(B, T, H * D)
