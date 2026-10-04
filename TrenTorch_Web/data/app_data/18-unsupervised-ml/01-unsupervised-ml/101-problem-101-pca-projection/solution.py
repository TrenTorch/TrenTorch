import numpy as np

def solve(X, components, k):
    """PCA projection is a linear coordinate change: for centered row data X and component matrix V, the retained coordinates are Z = X V[:, :k]."""
    return np.asarray(X) @ np.asarray(components)[:, :k]
