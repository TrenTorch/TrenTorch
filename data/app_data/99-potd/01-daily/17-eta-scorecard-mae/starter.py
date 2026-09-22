import numpy as np


def mae(y: np.ndarray, yhat: np.ndarray) -> float:
    """
    Mean absolute error.

    y, yhat: shape (n,), can be negative or positive; errors can point
    either direction.

    Return mean(|y - yhat|) over all n rows.
    """
    # TODO: np.abs applies elementwise regardless of which value is larger.
    pass
