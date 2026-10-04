import numpy as np

def solve(A, k):
    """Implement low-rank reconstruction according to the contract."""
    U, S, Vt = np.linalg.svd(np.asarray(A, float), full_matrices=False)
    k = min(max(int(k), 0), len(S))
    return U[:, :k] * S[:k] @ Vt[:k]
