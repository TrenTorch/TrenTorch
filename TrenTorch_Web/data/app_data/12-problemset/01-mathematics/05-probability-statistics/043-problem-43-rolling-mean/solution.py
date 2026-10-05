import numpy as np

def solve(x, window):
    x = np.asarray(x, dtype=float)
    result = np.full(len(x), np.nan)
    running_sum = 0.0
    for i, value in enumerate(x):
        running_sum += value
        if i >= window:
            running_sum -= x[i - window]
        if i >= window - 1:
            result[i] = running_sum / window
    return result
