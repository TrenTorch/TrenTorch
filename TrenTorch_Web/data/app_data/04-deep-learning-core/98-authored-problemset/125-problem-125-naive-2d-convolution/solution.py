import numpy as np

def solve(X, K):
    """Implement naive 2d convolution according to the contract."""
    X = np.asarray(X, float)
    K = np.asarray(K, float)
    H, W = X.shape
    kh, kw = K.shape
    out = np.empty((H - kh + 1, W - kw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = np.sum(X[i:i + kh, j:j + kw] * K)
    return out
