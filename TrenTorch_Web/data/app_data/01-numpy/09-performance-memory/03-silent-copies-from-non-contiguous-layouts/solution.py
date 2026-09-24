import numpy as np


def reshape_copies(arr: np.ndarray, new_shape: tuple) -> bool:
    result = arr.reshape(new_shape)
    return not np.shares_memory(arr, result)


def ravel_copies(arr: np.ndarray) -> bool:
    result = arr.ravel()
    return not np.shares_memory(arr, result)


def ensure_contiguous(arr: np.ndarray) -> np.ndarray:
    return np.ascontiguousarray(arr)


def reshape_write_propagates(arr: np.ndarray, new_shape: tuple, value: int) -> bool:
    result = arr.reshape(new_shape)
    result[:] = value
    return bool(np.all(arr == value))
