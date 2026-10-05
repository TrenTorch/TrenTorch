import numpy as np


def cooccurrence_matrix(token_ids: list[int], V: int, window: int) -> np.ndarray:
    """X[i, j] = sum of 1/distance over co-occurrences of j near i within `window`."""
    # TODO
    pass


def glove_weight(x, x_max: float, alpha: float) -> np.ndarray:
    """(x / x_max) ** alpha below x_max, 1 at or above it."""
    # TODO
    pass


def glove_loss(W, W_tilde, b, b_tilde, X, x_max: float, alpha: float) -> float:
    """Weighted squared error to log co-occurrence over pairs with X > 0."""
    # TODO
    pass
