import numpy as np


def are_broadcastable(shape_a: tuple, shape_b: tuple) -> bool:
    """
    Given two shape tuples, determine whether they are
    broadcast-compatible according to NumPy's rule: aligning
    from the trailing dimension, treating a missing leading
    dimension as size 1, and requiring each aligned pair to be
    either equal or have at least one side equal to 1.

    Implement this logic directly (do not just try the operation
    in NumPy and catch an exception).
    """
    pass


def broadcast_result_shape(shape_a: tuple, shape_b: tuple) -> tuple:
    """
    Given two broadcast-compatible shapes, compute and return
    the resulting broadcast shape, using the same alignment rule
    as are_broadcastable. Assume the shapes are compatible.
    """
    pass


def add_scalar(matrix: np.ndarray, scalar: float) -> np.ndarray:
    """
    Return matrix + scalar, relying on broadcasting.
    """
    pass


def add_row_vector(matrix: np.ndarray, row_vector: np.ndarray) -> np.ndarray:
    """
    Given a 2D matrix and a 1D row_vector whose length matches
    matrix's column count, return matrix + row_vector.
    """
    pass


def add_column_vector(matrix: np.ndarray, col_values: np.ndarray) -> np.ndarray:
    """
    Given a 2D matrix and a 1D col_values array whose length
    matches matrix's row count, add col_values[i] to every
    element of row i. You will need to reshape col_values to a
    column vector (using newaxis) before broadcasting will align
    it correctly against matrix's rows.
    """
    pass


def outer_sum(row_values: np.ndarray, col_values: np.ndarray) -> np.ndarray:
    """
    Given 1D arrays row_values (length n) and col_values
    (length m), return an (m, n) array where result[i, j] =
    col_values[i] + row_values[j], using broadcasting only
    (reshape each input appropriately, then add them).
    """
    pass
