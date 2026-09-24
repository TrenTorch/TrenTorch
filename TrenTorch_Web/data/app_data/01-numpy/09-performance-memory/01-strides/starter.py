import numpy as np


def compute_c_strides(shape: tuple, itemsize: int) -> tuple:
    """
    Return the strides tuple (in bytes) of a C-order array with the
    given `shape` and `itemsize`, using
        s_k = itemsize * product(shape[k+1:])
    Do not create an array to find this out.
    Example: compute_c_strides((3, 4), 8) -> (32, 8)
    """
    pass


def byte_offset(index: tuple, strides: tuple) -> int:
    """
    Return the byte offset of the element at `index` for an array
    with the given `strides`: the sum of index[k] * strides[k].
    `index` and `strides` have the same length.
    """
    pass


def slice_step_strides(arr: np.ndarray, step: int) -> tuple:
    """
    Return the strides that `arr[::step]` would have (slicing along
    axis 0 only), computed from arr.strides WITHOUT performing the
    slice. `step` may be positive or negative and is never 0.
    Works for arrays of any number of dimensions (>= 1).
    """
    pass
