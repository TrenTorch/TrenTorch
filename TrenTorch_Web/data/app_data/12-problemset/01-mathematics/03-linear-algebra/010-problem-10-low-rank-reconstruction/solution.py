import numpy as np

def solve(A, k):
    U, S, Vt = np.linalg.svd(np.asarray(A, dtype=float), full_matrices=False)
    rank = max(0, min(int(k), len(S)))
    return (U[:, :rank] * S[:rank]) @ Vt[:rank]
