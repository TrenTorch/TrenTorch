import numpy as np


def list_to_array(values: list) -> np.ndarray:
    return np.array(values)


def nested_list_to_array(rows: list) -> np.ndarray:
    return np.array(rows)


def make_zero_grid(rows: int, cols: int) -> np.ndarray:
    return np.zeros((rows, cols))


def make_filled_grid(rows: int, cols: int, fill_value) -> np.ndarray:
    return np.full((rows, cols), fill_value)


def make_ones_vector(length: int) -> np.ndarray:
    return np.ones(length)
