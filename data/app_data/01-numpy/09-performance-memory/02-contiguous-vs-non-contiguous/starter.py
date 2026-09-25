import numpy as np


def contiguity_flags(arr: np.ndarray) -> dict:
    """
    Return a dictionary with two keys:
      "c_contiguous": bool — arr.flags["C_CONTIGUOUS"]
      "f_contiguous": bool — arr.flags["F_CONTIGUOUS"]
    """
    pass


def contiguity_of_ops(arr: np.ndarray) -> dict:
    """
    `arr` is a 2D, C-contiguous array with at least 3 rows and at
    least 3 columns.

    Return a dictionary mapping each name below to a bool: whether the
    result of that operation is C-contiguous.

      "row_slice"         -> arr[1:3]
      "column_slice"      -> arr[:, 0]
      "step_slice"        -> arr[::2]
      "transpose"         -> arr.T
      "transpose_copy"    -> arr.T.copy()
    """
    pass
