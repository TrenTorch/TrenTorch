import numpy as np


def contrastive_loss(distances: np.ndarray, is_similar: np.ndarray, margin: float = 1.0) -> np.ndarray:
    """
    Elementwise s * d^2 + (1 - s) * max(0, margin - d)^2.
    Raise ValueError for mismatched shapes, negative distances, negative margin,
    or is_similar values other than 0 and 1.
    """
    pass
