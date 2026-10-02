import numpy as np


def matmul_from_scratch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    a is (m, k), b is (k, n): the inner dimensions must match. Returns
    an (m, n) result where entry (i, j) is the dot product of a's row i
    and b's column j:

        result[i, j] = sum_p(a[i, p] * b[p, j])

    Implement this with explicit loops over i and j (using the
    provided dot-product-style reduction for the inner sum is fine, a
    literal triple-nested loop is not required) rather than np.matmul
    or the @ operator: the point of this question is seeing the
    row-dot-column mechanism directly, once, before relying on a
    library to do it for the rest of the curriculum.
    """
    pass
