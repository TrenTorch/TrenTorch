import numpy as np


def list_to_array(values: list) -> np.ndarray:
    """
    Convert a flat Python list `values` into a 1-dimensional
    ndarray using np.array(), and return it.
    """
    pass


def nested_list_to_array(rows: list) -> np.ndarray:
    """
    Convert a list of equal-length lists `rows` into a
    2-dimensional ndarray using np.array(), and return it.
    Example: [[1, 2], [3, 4]] -> a 2x2 array.
    """
    pass


def make_zero_grid(rows: int, cols: int) -> np.ndarray:
    """
    Return a 2D array with `rows` rows and `cols` columns,
    every element equal to 0, using np.zeros.
    """
    pass


def make_filled_grid(rows: int, cols: int, fill_value) -> np.ndarray:
    """
    Return a 2D array with `rows` rows and `cols` columns,
    every element equal to `fill_value`, using np.full.
    """
    pass


def make_ones_vector(length: int) -> np.ndarray:
    """
    Return a 1D array of the given `length`, every element
    equal to 1, using np.ones.
    """
    pass
