import numpy as np

def solve(Z, components, k, mean):
    """PCA reconstruction maps retained coordinates back and restores the mean: X_hat = Z V[:, :k]^T + mean."""
    return np.asarray(Z) @ np.asarray(components)[:, :k].T + np.asarray(mean)
