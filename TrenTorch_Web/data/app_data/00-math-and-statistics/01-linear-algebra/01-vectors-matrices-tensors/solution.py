import numpy as np


def shape_of(x: np.ndarray) -> tuple:
    return x.shape


def ndim_of(x: np.ndarray) -> int:
    return x.ndim


def elementwise_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a + b


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a * b
