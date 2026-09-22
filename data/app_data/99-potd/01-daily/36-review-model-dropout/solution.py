import numpy as np


def inverted_dropout(x: np.ndarray, m: np.ndarray, p_keep: float) -> np.ndarray:
    return (x * m) / p_keep
