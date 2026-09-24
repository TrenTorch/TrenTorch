import numpy as np


def compute_summary(arr: np.ndarray) -> dict:
    return {
        "sum": arr.sum(),
        "mean": arr.mean(),
        "std": arr.std(),
        "min": arr.min(),
        "max": arr.max(),
        "argmin": arr.argmin(),
        "argmax": arr.argmax(),
    }


def sum_with_loop(arr: np.ndarray) -> float:
    total = 0
    for value in arr:
        total += value
    return total
