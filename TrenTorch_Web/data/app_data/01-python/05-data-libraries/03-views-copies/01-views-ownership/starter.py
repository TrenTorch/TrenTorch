import numpy as np


def is_view_of(candidate: np.ndarray, source: np.ndarray) -> bool:
    """
    Return True if `candidate` shares its underlying data buffer
    with `source` (i.e. `candidate` is a view into `source`'s
    memory, or vice versa, or both derive from the same buffer),
    False if they own completely independent buffers.

    Hint: np.shares_memory(a, b) answers exactly this question.
    """
    pass


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
