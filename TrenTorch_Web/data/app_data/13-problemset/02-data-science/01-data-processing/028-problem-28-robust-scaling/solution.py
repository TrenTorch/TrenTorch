import numpy as np

def solve(X):
    X = np.asarray(X, dtype=float)
    median = np.median(X, axis=0)
    q1 = np.quantile(X, .25, axis=0)
    q3 = np.quantile(X, .75, axis=0)
    iqr = q3 - q1
    return np.divide(X - median, iqr, out=np.zeros_like(X), where=iqr != 0)
