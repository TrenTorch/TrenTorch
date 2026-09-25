import numpy as np


def compute_summary(arr: np.ndarray) -> dict:
    """
    Return a dictionary with keys "sum", "mean", "std", "min",
    "max", "argmin", "argmax", each computed using the
    corresponding NumPy aggregation method on `arr` (assume arr
    is 1D for this function).
    """
    pass


def sum_with_loop(arr: np.ndarray) -> float:
    """
    Compute and return the sum of all elements in `arr` using an
    explicit Python for loop (not arr.sum()), to be compared
    against the vectorized version.
    """
    pass
