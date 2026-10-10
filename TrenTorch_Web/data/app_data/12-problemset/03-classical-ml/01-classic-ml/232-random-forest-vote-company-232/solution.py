import numpy as np

def solve(P):
    P = np.asarray(P, dtype=float)
    mean = P.mean(axis=0)
    return int(np.argmax(mean))
