import numpy as np

def solve(error):
    e = float(error)
    if not 0 < e < 1:
        raise ValueError("error must lie strictly between 0 and 1")
    return 0.5 * np.log((1 - e) / e)
