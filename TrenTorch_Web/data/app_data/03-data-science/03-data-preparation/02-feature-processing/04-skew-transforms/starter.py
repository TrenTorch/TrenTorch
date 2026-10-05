import numpy as np


def skewness(x: np.ndarray) -> float:
    """
    x: 1D float array

    Returns:
        mean(((x - mean) / std) ** 3) with std the population standard
        deviation, as a float. Returns 0.0 when std is zero.
    """
    # TODO: Implement the formula from Theory.
    pass


def log1p_transform(x: np.ndarray) -> np.ndarray:
    """
    Returns log(1 + x) for a 1D array with no negative values.

    Raises:
        ValueError: if any value is negative.
    """
    # TODO: Use np.log1p.
    pass


def inverse_log1p(z: np.ndarray) -> np.ndarray:
    """Returns exp(z) - 1, the inverse of log1p_transform."""
    # TODO: Use np.expm1.
    pass


def box_cox(x: np.ndarray, lam: float) -> np.ndarray:
    """
    x: 1D float array of strictly positive values
    lam: the Box-Cox parameter

    Returns:
        (x ** lam - 1) / lam when lam != 0, and log(x) when lam == 0.

    Raises:
        ValueError: if any value is not strictly positive.
    """
    # TODO: Implement both branches from Theory.
    pass


def best_box_cox_lambda(x: np.ndarray, candidates: list) -> float:
    """
    Returns the value in `candidates` whose Box-Cox transform of x has
    the smallest absolute skewness. Ties go to the earliest candidate.
    """
    # TODO: Compare the skewness of each transform.
    pass
