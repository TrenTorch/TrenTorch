import numpy as np


def omp(D: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    """
    Orthogonal matching pursuit: return a length-d coefficient vector with at
    most k nonzero entries such that D @ x approximates y. Raises ValueError
    for a shape mismatch or k outside 0..d.
    """
    pass
