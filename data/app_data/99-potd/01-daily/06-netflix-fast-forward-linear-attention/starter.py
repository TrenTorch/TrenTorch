import numpy as np


def feature_map(x: np.ndarray) -> np.ndarray:
    """
    The element-wise positive feature map applied to both Q and K:

        phi(x) = max(x, 0) + 1

    Returns an array of the same shape as x. Every output element is >= 1.
    """
    pass


def linear_attention_row_sums(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Linear attention over one user's interaction sequence, WITHOUT ever
    materializing an N x N matrix.

    Q, K, V: float arrays of shape (N, d). N can reach 100_000.

    With Q' = phi(Q) and K' = phi(K), row i of the attention output is

        O_i = (Q'_i @ M) / (Q'_i @ Z)

    where M = K'^T @ V is d x d and Z = sum_j K'_j is a d-vector.

    Returns a float array of shape (N,): entry i is the SUM of the elements
    of row i of O (not the full N x d matrix).

    Memory must stay O(N * d). Any intermediate of shape (N, N) is a failure.
    """
    # TODO: see Theory for how to reorder the multiplications.
    pass
