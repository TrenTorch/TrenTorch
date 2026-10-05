import numpy as np


def distinct(a: np.ndarray) -> np.ndarray:
    return np.unique(a)


def value_counts(a: np.ndarray):
    values, counts = np.unique(a, return_counts=True)
    return values, counts


def first_positions(a: np.ndarray) -> np.ndarray:
    return np.unique(a, return_index=True)[1]


def codes(a: np.ndarray) -> np.ndarray:
    return np.unique(a, return_inverse=True)[1].reshape(np.shape(a))


def mode(a: np.ndarray):
    values, counts = np.unique(a, return_counts=True)
    return values[np.argmax(counts)]


def unique_in_order(a: np.ndarray) -> np.ndarray:
    _, index = np.unique(a, return_index=True)
    return np.asarray(a)[np.sort(index)]
