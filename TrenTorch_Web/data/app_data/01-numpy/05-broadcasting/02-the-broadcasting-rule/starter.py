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
