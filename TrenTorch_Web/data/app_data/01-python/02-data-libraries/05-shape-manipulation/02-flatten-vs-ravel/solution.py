import numpy as np


def flatten_safe(arr: np.ndarray) -> np.ndarray:
    return arr.flatten()


def flatten_efficient(arr: np.ndarray) -> np.ndarray:
    return arr.ravel()


def compare_flatten_ravel(arr: np.ndarray) -> dict:
    f = arr.flatten()
    r = arr.ravel()
    return {
        "flatten_result": f,
        "ravel_result": r,
        "flatten_shares_memory": bool(np.shares_memory(arr, f)),
        "ravel_shares_memory": bool(np.shares_memory(arr, r)),
    }
