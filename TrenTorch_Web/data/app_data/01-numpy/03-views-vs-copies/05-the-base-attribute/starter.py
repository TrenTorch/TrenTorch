import numpy as np


def owns_its_data(arr: np.ndarray) -> bool:
    """
    Return True if `arr` owns its own data buffer (its .base is
    None), False if it is a view of some other array.
    """
    pass


def find_ultimate_owner(arr: np.ndarray) -> np.ndarray:
    """
    Given an array `arr` that may be a view of a view of a view
    (any depth), follow the .base chain until reaching the array
    that owns its own data (.base is None), and return that
    array. If `arr` already owns its data, return `arr` itself.
    """
    pass
