import numpy as np


def basic_slice(a: np.ndarray, start: int, stop: int) -> np.ndarray:
    return a[start:stop]


def boolean_mask(a: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return a[mask]


def fancy_index(a: np.ndarray, indices: np.ndarray) -> np.ndarray:
    return a[indices]


def is_a_view_of(child: np.ndarray, parent: np.ndarray) -> bool:
    return np.shares_memory(child, parent)
