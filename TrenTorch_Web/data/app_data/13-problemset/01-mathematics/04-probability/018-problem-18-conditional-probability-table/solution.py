import numpy as np

def solve(A, B):
    A = np.asarray(A, dtype=bool)
    B = np.asarray(B, dtype=bool)
    denominator = np.sum(B)
    return 0.0 if denominator == 0 else float(np.sum(A & B) / denominator)
