import numpy as np

def solve(x, sublayer):
    values = np.asarray(x)
    return values + np.asarray(sublayer(values))
