import numpy as np


def join_along_existing_axis(arrays: list, axis: int) -> np.ndarray:
    return np.concatenate(arrays, axis=axis)


def stack_as_new_axis(arrays: list) -> np.ndarray:
    return np.stack(arrays)


def side_by_side(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.hstack([a, b])


def stacked_vertically(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.vstack([a, b])
