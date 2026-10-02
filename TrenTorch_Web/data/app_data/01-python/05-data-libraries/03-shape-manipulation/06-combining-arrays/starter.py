import numpy as np


def join_along_existing_axis(arrays: list, axis: int) -> np.ndarray:
    """
    Join the arrays in `arrays` along the given existing `axis`
    using np.concatenate. All arrays share the same number of
    dimensions and matching sizes on every axis except `axis`.
    """
    pass


def stack_as_new_axis(arrays: list) -> np.ndarray:
    """
    Combine the arrays in `arrays` (all of identical shape) into
    a single array with one new leading axis, using np.stack.
    """
    pass


def side_by_side(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Join 2D arrays `a` and `b` side by side (matching row counts)
    using np.hstack.
    """
    pass


def stacked_vertically(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Join 2D arrays `a` and `b` on top of each other (matching
    column counts) using np.vstack.
    """
    pass
