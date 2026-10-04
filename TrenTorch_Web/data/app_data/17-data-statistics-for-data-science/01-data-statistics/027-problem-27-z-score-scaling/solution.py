import numpy as np

def solve(x):
    """Implement z-score scaling according to the contract."""
    X = np.asarray(x, float)
    mu, sd = (X.mean(0), X.std(0))
    return np.divide(X - mu, sd, out=np.zeros_like(X), where=sd != 0)
