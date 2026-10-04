import numpy as np

def solve(Z, components, k, mean):
    """Implement pca reconstruction according to the contract."""
    return np.asarray(Z) @ np.asarray(components)[:, :k].T + np.asarray(mean)
