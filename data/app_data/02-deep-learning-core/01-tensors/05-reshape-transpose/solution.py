import numpy as np


def reshape(a: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    return a.reshape(shape)


def transpose(a: np.ndarray, dim0: int, dim1: int) -> np.ndarray:
    return np.swapaxes(a, dim0, dim1)


def permute(a: np.ndarray, dims: tuple[int, ...]) -> np.ndarray:
    return np.transpose(a, dims)
