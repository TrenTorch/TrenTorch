import numpy as np


def skewness(x: np.ndarray) -> float:
    """
    Pearson's moment coefficient of skewness: the average CUBED
    z-score of every value.

        skew(x) = mean(((x - mean(x)) / std(x))^3)

    Cubing (rather than squaring, like variance does) preserves sign:
    a distribution with a long right tail gives a positive number, a
    long left tail gives a negative one, a symmetric distribution
    gives (near) zero.
    """
    pass


def summarize_distribution(x: np.ndarray) -> dict:
    """
    Returns {"mean": ..., "median": ..., "std": ..., "skew": ...},
    the standard quick summary of a feature's distribution. `skewness`
    is already provided above.
    """
    pass
