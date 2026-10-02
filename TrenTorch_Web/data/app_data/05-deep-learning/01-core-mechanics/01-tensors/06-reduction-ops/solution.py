import numpy as np


def sum_(a: np.ndarray, axis: int | None = None, keepdims: bool = False) -> np.ndarray:
    return np.sum(a, axis=axis, keepdims=keepdims)


def mean_(a: np.ndarray, axis: int | None = None, keepdims: bool = False) -> np.ndarray:
    return np.mean(a, axis=axis, keepdims=keepdims)


def max_(a: np.ndarray, axis: int | None = None, keepdims: bool = False):
    if axis is None:
        return np.max(a)
    values = np.max(a, axis=axis, keepdims=keepdims)
    indices = np.argmax(a, axis=axis, keepdims=keepdims)
    return values, indices
