import numpy as np


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a * b


def increment_in_place(arr: np.ndarray, amount: float) -> None:
    arr += amount


def square_each(arr: np.ndarray) -> np.ndarray:
    return arr**2


def sqrt_all(arr: np.ndarray) -> np.ndarray:
    return np.sqrt(arr)


def exponentiate(arr: np.ndarray) -> np.ndarray:
    return np.exp(arr)


def natural_log(arr: np.ndarray) -> np.ndarray:
    return np.log(arr)


def absolute_values(arr: np.ndarray) -> np.ndarray:
    return np.abs(arr)
