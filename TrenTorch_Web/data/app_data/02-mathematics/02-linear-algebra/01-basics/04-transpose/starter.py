import numpy as np


def transpose(x: np.ndarray) -> np.ndarray:
    """
    Mirrors x.T (equivalently torch.t(x) for 2D, or x.transpose(0, 1)):
    flips a matrix over its diagonal, so entry (i, j) becomes (j, i)
    and an (m, n) matrix becomes (n, m).
    """
    pass


def is_a_view_of(original: np.ndarray, derived: np.ndarray) -> bool:
    """
    Transpose does NOT copy data: it returns a new array object that
    shares the same underlying memory buffer as the original, just
    read in a different order (a different "stride" pattern). Returns
    True iff `derived` and `original` share memory (np.shares_memory
    is provided for exactly this check).
    """
    pass
