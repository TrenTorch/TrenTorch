import numpy as np


def remove_all_singleton_dims(arr: np.ndarray) -> np.ndarray:
    return arr.squeeze()


def remove_singleton_at(arr: np.ndarray, axis: int) -> np.ndarray:
    return arr.squeeze(axis=axis)
