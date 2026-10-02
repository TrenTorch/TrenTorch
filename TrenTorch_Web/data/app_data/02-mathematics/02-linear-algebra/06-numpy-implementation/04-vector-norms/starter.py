import numpy as np


def l2_norm_from_scratch(v: np.ndarray) -> float:
    """
    Compute the Euclidean (L2) norm of 1D vector v directly from
    its definition (sum of squares, then square root), without
    calling np.linalg.norm. You may use np.sqrt and np.sum.
    """
    pass


def l2_norm_builtin(v: np.ndarray) -> float:
    """
    Compute the same result as l2_norm_from_scratch, using
    np.linalg.norm directly.
    """
    pass


def normalize_vector(v: np.ndarray) -> np.ndarray:
    """
    Return a new vector pointing in the same direction as v, but
    with an L2 norm of exactly 1 (a "unit vector"). Do not
    mutate v.
    """
    pass
