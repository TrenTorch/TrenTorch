import numpy as np

def solve(X, gamma, beta, eps=1e-05):
    """Implement layer normalization according to the contract."""
    X = np.asarray(X, float)
    mu = X.mean(1, keepdims=True)
    var = X.var(1, keepdims=True)
    return gamma * (X - mu) / np.sqrt(var + eps) + beta
