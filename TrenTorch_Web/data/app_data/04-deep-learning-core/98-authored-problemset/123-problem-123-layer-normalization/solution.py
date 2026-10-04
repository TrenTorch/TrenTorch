import numpy as np

def solve(X, gamma, beta, eps=1e-5):
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=1, keepdims=True)
    variance = X.var(axis=1, keepdims=True)
    normalized = (X - mean) / np.sqrt(variance + eps)
    return np.asarray(gamma) * normalized + np.asarray(beta)
