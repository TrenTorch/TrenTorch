import numpy as np

def solve(X, y, knots):
    """Implement universal approximation toy basis according to the contract."""
    B = np.maximum(np.asarray(X)[:, None] - np.asarray(knots)[None, :], 0)
    w = np.linalg.lstsq(B, np.asarray(y), rcond=None)[0]
    return (B @ w, w)
