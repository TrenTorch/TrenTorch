import math

import numpy as np


def describe_shape(arr: np.ndarray) -> dict:
    return {"shape": arr.shape, "ndim": arr.ndim, "size": arr.size}


def is_shape_valid_for_size(shape: tuple, total_elements: int) -> bool:
    return math.prod(shape) == total_elements
