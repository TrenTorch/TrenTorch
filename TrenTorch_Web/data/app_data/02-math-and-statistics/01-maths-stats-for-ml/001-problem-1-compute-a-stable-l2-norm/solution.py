import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    scale = np.max(np.abs(x))
    return 0.0 if scale == 0 else float(scale * np.sqrt(np.sum((x / scale) ** 2)))
