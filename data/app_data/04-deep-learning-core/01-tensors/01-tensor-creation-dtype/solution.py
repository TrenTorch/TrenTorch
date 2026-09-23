import numpy as np


def make_tensor(data, dtype: np.dtype | None = None) -> np.ndarray:
    array = np.array(data)
    if dtype is not None:
        return array.astype(dtype)
    if np.issubdtype(array.dtype, np.floating):
        return array.astype(np.float32)
    return array


def zeros(shape: tuple[int, ...], dtype: np.dtype = np.float32) -> np.ndarray:
    return np.zeros(shape, dtype=dtype)


def ones(shape: tuple[int, ...], dtype: np.dtype = np.float32) -> np.ndarray:
    return np.ones(shape, dtype=dtype)


def arange(start: float, stop: float, step: float = 1, dtype: np.dtype | None = None) -> np.ndarray:
    result = np.arange(start, stop, step)
    if dtype is not None:
        return result.astype(dtype)
    if np.issubdtype(result.dtype, np.floating):
        return result.astype(np.float32)
    return result
