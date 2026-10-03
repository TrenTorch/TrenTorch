import numpy as np


def join_along_existing_axis(arrays: list, axis: int) -> np.ndarray:
    return np.concatenate(arrays, axis=axis)


def stack_as_new_axis(arrays: list) -> np.ndarray:
    return np.stack(arrays)


def side_by_side(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.hstack([a, b])


def stacked_vertically(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.vstack([a, b])


def split_into_n_parts(arr: np.ndarray, n: int, axis: int) -> list:
    return np.split(arr, n, axis=axis)


def split_columns(arr: np.ndarray, n: int) -> list:
    return np.hsplit(arr, n)


def split_result_shares_memory(arr: np.ndarray, n: int, axis: int) -> bool:
    parts = np.split(arr, n, axis=axis)
    return bool(np.shares_memory(parts[0], arr))
