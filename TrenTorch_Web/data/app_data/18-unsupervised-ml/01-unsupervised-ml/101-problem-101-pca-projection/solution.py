import numpy as np

def solve(X, components, k):
    """Implement pca projection according to the contract."""
    return np.asarray(X) @ np.asarray(components)[:, :k]
