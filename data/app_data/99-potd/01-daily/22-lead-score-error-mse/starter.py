import numpy as np


def mse(y: np.ndarray, yhat: np.ndarray) -> float:
    """
    Mean squared error.

    y, yhat: shape (n,).

    Return mean((y - yhat) ** 2): square each row's error first, then
    average. Averaging the raw errors first and squaring afterward is a
    different (wrong) computation.
    """
    # TODO: diff ** 2 elementwise, then .mean() over the whole batch.
    pass
