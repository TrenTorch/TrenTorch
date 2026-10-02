import numpy as np


def select_by_indices(arr: np.ndarray, indices: list) -> np.ndarray:
    """
    Return a new array containing the elements of `arr` at the
    positions given in `indices`, in the order given (which may
    reorder or repeat positions), using fancy indexing.
    """
    pass


def select_paired_2d(arr: np.ndarray, rows: list, cols: list) -> np.ndarray:
    """
    Given a 2D array `arr` and equal-length lists `rows` and
    `cols`, return a 1D array where each element is
    arr[rows[i], cols[i]] for each position i, using fancy
    indexing (not a loop).
    """
    pass


def fancy_index_is_copy(arr: np.ndarray, indices: list) -> dict:
    """
    Select elements at `indices` from `arr` using fancy indexing,
    then mutate the first element of the result to -1.

    Return a dictionary:
      {
        "selected": <the fancy-indexed result, after mutation>,
        "original_unaffected": <True if arr itself was NOT
                                  changed by the mutation above>
      }
    """
    pass
