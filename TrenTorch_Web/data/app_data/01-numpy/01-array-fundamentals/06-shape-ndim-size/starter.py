import numpy as np


def describe_shape(arr: np.ndarray) -> dict:
    """
    Return a dictionary with three keys: "shape", "ndim", "size",
    reporting the corresponding attributes of `arr` directly.
    """
    pass


def is_shape_valid_for_size(shape: tuple, total_elements: int) -> bool:
    """
    Given a candidate `shape` tuple and a required total element
    count `total_elements`, return True if the product of all
    values in `shape` equals `total_elements`, False otherwise.
    This mirrors the validity check NumPy performs internally
    before allowing a reshape.
    """
    pass
