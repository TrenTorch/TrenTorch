import numpy as np


def oblique_split_gain(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float) -> float:
    """
    Gini gain of the split X @ w + b <= 0 versus > 0.
    Raise ValueError for shape mismatches or w equal to the zero vector.
    """
    pass
