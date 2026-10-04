import numpy as np

def solve(X, n_heads):
    """Implement multi-head attention split according to the contract."""
    X = np.asarray(X)
    B, T, D = X.shape
    if D % n_heads:
        raise ValueError('embedding dimension must divide n_heads')
    return X.reshape(B, T, n_heads, D // n_heads).transpose(0, 2, 1, 3)
