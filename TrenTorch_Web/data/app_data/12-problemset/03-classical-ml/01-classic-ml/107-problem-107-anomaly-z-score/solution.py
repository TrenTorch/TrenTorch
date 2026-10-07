import numpy as np

def solve(x, threshold=3):
    x = np.asarray(x, dtype=float)
    mu = x.mean(axis=0)
    sd = x.std(axis=0)
    z = np.divide(x - mu, sd, out=np.zeros_like(x), where=sd != 0)
    return np.abs(z) > threshold
