import numpy as np


def reshape_to(arr: np.ndarray, new_shape: tuple) -> np.ndarray:
    return arr.reshape(new_shape)


def reshape_with_inferred_dim(arr: np.ndarray, known_dim: int) -> np.ndarray:
    return arr.reshape((-1, known_dim))


def reshape_shares_memory(arr: np.ndarray, new_shape: tuple) -> bool:
    result = arr.reshape(new_shape)
    return bool(np.shares_memory(arr, result))


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
