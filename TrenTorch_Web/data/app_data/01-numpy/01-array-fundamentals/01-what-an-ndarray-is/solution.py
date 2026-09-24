import numpy as np


def describe_ndarray_basics(arr: np.ndarray) -> dict:
    return {"dtype": str(arr.dtype), "itemsize": arr.itemsize}
