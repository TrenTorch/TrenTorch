import numpy as np

def solve(f, samples):
    samples = np.asarray(samples, dtype=float)
    return float(np.mean(f(samples)))
