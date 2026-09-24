import numpy as np


def predict_broadcast_shape(shape_a: tuple, shape_b: tuple) -> tuple:
    length = max(len(shape_a), len(shape_b))
    padded_a = (1,) * (length - len(shape_a)) + tuple(shape_a)
    padded_b = (1,) * (length - len(shape_b)) + tuple(shape_b)

    result = []
    for a, b in zip(padded_a, padded_b):
        if a == b or a == 1 or b == 1:
            result.append(max(a, b))
        else:
            raise ValueError(f"shapes {shape_a} and {shape_b} are not broadcast-compatible")
    return tuple(result)


def classify_by_memory(op, arr: np.ndarray) -> str:
    result = op(arr)
    return "view" if np.shares_memory(result, arr) else "copy"


def standardize_columns(arr: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    column_mean = arr.mean(axis=0)
    column_std = arr.std(axis=0)
    return (arr - column_mean) / (column_std + eps)
