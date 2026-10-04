import numpy as np

def solve(x):
    """Implement robust scaling according to the contract."""
    X = np.asarray(x, float)
    med, q1, q3 = (np.median(X, 0), np.quantile(X, 0.25, 0), np.quantile(X, 0.75, 0))
    iqr = q3 - q1
    return np.divide(X - med, iqr, out=np.zeros_like(X), where=iqr != 0)
