import numpy as np

def solve(X):
    """Implement pca centering according to the contract."""
    X = np.asarray(X, float)
    return X - X.mean(0)
