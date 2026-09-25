import numpy as np


def select_by_indices(arr: np.ndarray, indices: list) -> np.ndarray:
    return arr[indices]


def select_paired_2d(arr: np.ndarray, rows: list, cols: list) -> np.ndarray:
    return arr[rows, cols]


def fancy_index_is_copy(arr: np.ndarray, indices: list) -> dict:
    original_snapshot = arr.copy()
    selected = arr[indices]
    selected[0] = -1
    return {
        "selected": selected,
        "original_unaffected": bool(np.array_equal(arr, original_snapshot)),
    }
