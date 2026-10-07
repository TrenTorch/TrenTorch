import numpy as np

def solve(x, a, b):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not np.all((x == 0) | (x == 1)):
        raise ValueError("x must be a 1-D sequence of 0/1 values")
    if a < 1 or b < 1:
        raise ValueError("a and b must be >= 1 for the Beta mode to be defined")
    a_post = a + np.sum(x)
    b_post = b + len(x) - np.sum(x)
    if a_post + b_post == 2:
        raise ValueError("posterior is Beta(1, 1): mode is not unique")
    return float((a_post - 1) / (a_post + b_post - 2))
