import numpy as np


def to_column_vector(arr: np.ndarray) -> np.ndarray:
    """
    Given a 1D array `arr` of shape (n,), return it reshaped to
    shape (n, 1), a column vector, using np.newaxis.
    """
    pass


def to_row_vector(arr: np.ndarray) -> np.ndarray:
    """
    Given a 1D array `arr` of shape (n,), return it reshaped to
    shape (1, n), a row vector, using np.newaxis.
    """
    pass


def add_dimension_at(arr: np.ndarray, axis: int) -> np.ndarray:
    """
    Insert a new dimension of size 1 into `arr` at position
    `axis`, using np.expand_dims.
    """
    pass


def remove_all_singleton_dims(arr: np.ndarray) -> np.ndarray:
    """
    Return `arr` with every dimension of size 1 removed, using
    squeeze() with no arguments.
    """
    pass


def remove_singleton_at(arr: np.ndarray, axis: int) -> np.ndarray:
    """
    Return `arr` with the size-1 dimension at position `axis`
    removed, using squeeze(axis=axis). Assume the given axis
    does have size 1.
    """
    pass
