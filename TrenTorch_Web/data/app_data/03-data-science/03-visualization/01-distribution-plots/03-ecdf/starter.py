import numpy as np


def ecdf(x: np.ndarray) -> tuple:
    """
    Returns (values, probabilities): x sorted ascending and
    probabilities[i] = (i + 1) / n. Repeated values each get an entry.
    """
    # TODO: Sort the data and pair it with the staircase heights.
    pass


def ecdf_at(x: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    Returns a float array: for each query point, the fraction of entries
    of x that are less than or equal to it.
    """
    # TODO: Count the sorted values at or below each point.
    pass


def ks_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    Returns max over t of |F_x(t) - F_y(t)|, with F the ECDF of each
    sample, as a float. Only the pooled sample values need checking.
    """
    # TODO: Compare the two ECDFs at every pooled value.
    pass
