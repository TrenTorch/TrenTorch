import numpy as np


def reshape_to(arr: np.ndarray, new_shape: tuple) -> np.ndarray:
    return arr.reshape(new_shape)


def reshape_with_inferred_dim(arr: np.ndarray, known_dim: int) -> np.ndarray:
    return arr.reshape((-1, known_dim))


def reshape_shares_memory(arr: np.ndarray, new_shape: tuple) -> bool:
    result = arr.reshape(new_shape)
    return bool(np.shares_memory(arr, result))
