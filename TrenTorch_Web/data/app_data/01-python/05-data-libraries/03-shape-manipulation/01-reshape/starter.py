import numpy as np


def reshape_to(arr: np.ndarray, new_shape: tuple) -> np.ndarray:
    """
    Return `arr` reshaped to `new_shape`, using .reshape().
    Assume new_shape's product matches arr.size.
    """
    pass


def reshape_with_inferred_dim(arr: np.ndarray, known_dim: int) -> np.ndarray:
    """
    Reshape `arr` (1D) into a 2D array with `known_dim` columns,
    letting NumPy infer the number of rows automatically using -1.
    """
    pass


def reshape_shares_memory(arr: np.ndarray, new_shape: tuple) -> bool:
    """
    Reshape `arr` to `new_shape`, and return True if the result
    shares memory with `arr` (a view was returned), False if it
    does not (a copy was returned). Use np.shares_memory to check
    the actual outcome rather than assuming.
    """
    pass
