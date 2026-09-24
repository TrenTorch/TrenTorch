import numpy as np


def get_element_1d(arr: np.ndarray, index: int):
    return arr[index]


def get_element_2d(arr: np.ndarray, row: int, col: int):
    return arr[row, col]


def get_row(arr: np.ndarray, row: int) -> np.ndarray:
    return arr[row]
