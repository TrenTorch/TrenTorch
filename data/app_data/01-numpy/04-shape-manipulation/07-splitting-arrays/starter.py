import numpy as np


def split_into_n_parts(arr: np.ndarray, n: int, axis: int) -> list:
    """
    Split `arr` into `n` equal parts along `axis`, using
    np.split, and return the resulting list of sub-arrays.
    """
    pass


def split_columns(arr: np.ndarray, n: int) -> list:
    """
    Split 2D array `arr` into `n` equal column-groups, using
    np.hsplit, and return the resulting list.
    """
    pass


def split_result_shares_memory(arr: np.ndarray, n: int, axis: int) -> bool:
    """
    Split `arr` into `n` parts along `axis` using np.split, and
    return True if the FIRST resulting sub-array shares memory
    with `arr` (checked via np.shares_memory), False otherwise.
    """
    pass
