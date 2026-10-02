import numpy as np


def svd(a: np.ndarray):
    """
    Mirrors np.linalg.svd(a, full_matrices=False) / torch.linalg.svd:
    factors ANY matrix `a` (m, n), square or not, as:

        a = U @ diag(singular_values) @ Vt

    where U is (m, r), singular_values is length r (sorted descending),
    Vt is (r, n), and r = min(m, n) (the "economy"/"reduced" size,
    full_matrices=False). Returns (u, singular_values, vt).
    """
    pass


def reconstruct_from_svd(u: np.ndarray, singular_values: np.ndarray, vt: np.ndarray) -> np.ndarray:
    """
    Rebuilds the original matrix from its SVD factors:

        a = u @ diag(singular_values) @ vt
    """
    pass


def low_rank_approximation(a: np.ndarray, k: int) -> np.ndarray:
    """
    Keeps only the k largest singular values (and their corresponding
    columns/rows of u and vt), then reconstructs. Because
    np.linalg.svd already returns singular values sorted descending,
    "the k largest" is just "the first k".

    This is the best possible rank-k approximation of `a` (in the
    sense of minimizing squared reconstruction error, the Eckart-Young
    theorem), the same idea PCA (06-unsupervised) uses to compress data
    onto its most informative directions.
    """
    pass
