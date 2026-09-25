import numpy as np


def slice_1d(arr: np.ndarray, start: int, stop: int, step: int = 1) -> np.ndarray:
    return arr[start:stop:step]


def extract_submatrix(
    arr: np.ndarray, row_start: int, row_stop: int, col_start: int, col_stop: int
) -> np.ndarray:
    return arr[row_start:row_stop, col_start:col_stop]


def slice_shares_memory(arr: np.ndarray, start: int, stop: int) -> dict:
    sl = arr[start:stop]
    sl[0] = -1
    return {
        "slice_result": sl,
        "original_array": arr,
        "original_was_affected": bool(arr[start] == -1),
    }
