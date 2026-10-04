import numpy as np

def solve(x, degree):
    x = np.asarray(x, dtype=float)
    if degree == 0:
        return np.empty((x.size, 0), dtype=float)
    return np.column_stack([x ** power for power in range(1, degree + 1)])
