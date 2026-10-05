import numpy as np


def slice_1d(arr: np.ndarray, start: int, stop: int, step: int = 1) -> np.ndarray:
    """
    Return the slice of `arr` from `start` to `stop` (exclusive)
    with the given `step`, using standard slice syntax.
    """
    pass


def extract_submatrix(
    arr: np.ndarray, row_start: int, row_stop: int, col_start: int, col_stop: int
) -> np.ndarray:
    """
    Return the sub-matrix of 2D array `arr` spanning rows
    [row_start:row_stop) and columns [col_start:col_stop).
    """
    pass


def slice_shares_memory(arr: np.ndarray, start: int, stop: int) -> dict:
    """
    Take a slice of `arr` from `start` to `stop`, then mutate the
    FIRST element of that slice to the value -1.

    Return a dictionary:
      {
        "slice_result": <the slice, after mutation>,
        "original_array": <arr itself, after the mutation above>,
        "original_was_affected": <True if arr's corresponding
                                    element is now also -1>
      }
    """
    pass
