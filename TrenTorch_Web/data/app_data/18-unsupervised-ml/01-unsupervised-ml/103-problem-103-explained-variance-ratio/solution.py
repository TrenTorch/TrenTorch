import numpy as np

def solve(eigenvalues):
    """Implement explained variance ratio according to the contract."""
    e = np.asarray(eigenvalues, float)
    return e / e.sum()
