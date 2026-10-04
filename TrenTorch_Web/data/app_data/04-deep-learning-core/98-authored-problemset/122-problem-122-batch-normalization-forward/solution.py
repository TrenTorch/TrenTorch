import numpy as np

def solve(X, gamma, beta, eps=1e-05):
    """Implement batch normalization forward according to the contract."""
    X = np.asarray(X, float)
    mu = X.mean(0)
    var = X.var(0)
    return gamma * (X - mu) / np.sqrt(var + eps) + beta
