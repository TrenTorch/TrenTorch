import numpy as np


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a * b


def increment_in_place(arr: np.ndarray, amount: float) -> None:
    arr += amount


def square_each(arr: np.ndarray) -> np.ndarray:
    return arr**2
