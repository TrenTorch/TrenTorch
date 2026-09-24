import numpy as np


def predict_broadcast_shape(shape_a: tuple, shape_b: tuple) -> tuple:
    """
    Return the shape that results from broadcasting shapes `shape_a`
    and `shape_b` together, following the rule from Module 5:
    align from the trailing axis; two dimensions are compatible if they
    are equal or one is 1; a missing leading dimension counts as 1.

    Raise ValueError if the shapes are incompatible.
    Implement the rule yourself — do not call np.broadcast_shapes,
    np.broadcast_arrays, or perform an actual array operation.
    Examples:
        (3, 1) with (1, 4) -> (3, 4)
        (5,)   with (2, 5) -> (2, 5)
        (3,)   with (4,)   -> raises ValueError
    """
    pass


def classify_by_memory(op, arr: np.ndarray) -> str:
    """
    `op` is a function that takes an ndarray and returns an ndarray.
    Apply it to `arr` and return "view" if the result shares memory
    with `arr` (np.shares_memory), or "copy" if it does not.
    Do not modify `arr`.
    """
    pass


def standardize_columns(arr: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """
    `arr` is a 2D float array of shape (rows, cols). Return a new array
    of the same shape in which each COLUMN has been shifted to mean 0
    and scaled by its standard deviation:
        (arr - column_mean) / (column_std + eps)
    Use axis-based aggregation and broadcasting; no Python loops.
    A column with zero variance must give all zeros, not NaN.
    `arr` must not be modified.
    """
    pass
