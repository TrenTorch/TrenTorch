import numpy as np

def solve(A, B):
    """Implement conditional probability table according to the contract."""
    A, B = (np.asarray(A, bool), np.asarray(B, bool))
    den = np.sum(B)
    return 0.0 if den == 0 else float(np.sum(A & B) / den)
