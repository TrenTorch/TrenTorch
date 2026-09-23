import numpy as np


def transpose(x: np.ndarray) -> np.ndarray:
    return x.T


def is_a_view_of(original: np.ndarray, derived: np.ndarray) -> bool:
    return np.shares_memory(original, derived)
