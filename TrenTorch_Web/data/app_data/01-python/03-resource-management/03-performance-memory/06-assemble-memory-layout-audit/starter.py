import time

import numpy as np


def audit_array(arr: np.ndarray, new_shape: tuple) -> dict:
    """
    `arr` is a 2D array (it may be a view, a transpose, or a slice) with
    no dimensions of size 1. `new_shape` is a valid shape for arr.size
    elements.

    Return a dictionary with these keys:
      "strides":            arr.strides
      "expected_c_strides": the strides a C-order array of arr's shape
                            and itemsize would have (compute from
                            arr.shape and arr.itemsize, not from arr.strides)
      "nbytes":             arr.nbytes
      "c_contiguous":       bool, arr.flags["C_CONTIGUOUS"]
      "reshape_copies":     bool, True if arr.reshape(new_shape) copies
      "contiguous_version": a C-contiguous array with the same values as
                            arr, copying only if arr is not already
                            C-contiguous
      "conversion_copied":  bool, True if "contiguous_version" does NOT
                            share memory with arr
      "sum_matches":        bool, True if the total of all elements
                            computed with nested Python for loops (loop
                            over rows, then over elements of each row)
                            equals arr.sum() (use np.isclose)
      "speedup":            float, (best time of the nested-loop total)
                            / (best time of arr.sum()), each measured
                            over 3 repeats with time.perf_counter()
    """
    pass
