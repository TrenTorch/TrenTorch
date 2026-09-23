import numpy as np


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a + b


def sub(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a - b


def mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a * b


def div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.true_divide(a, b)


def power(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a**b
