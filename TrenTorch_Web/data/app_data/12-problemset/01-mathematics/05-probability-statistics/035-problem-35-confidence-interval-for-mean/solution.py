import numpy as np

def solve(x, critical=1.96):
    x = np.asarray(x, dtype=float)
    se = np.std(x, ddof=1) / np.sqrt(len(x))
    mean = x.mean()
    return float(mean - critical * se), float(mean + critical * se)
