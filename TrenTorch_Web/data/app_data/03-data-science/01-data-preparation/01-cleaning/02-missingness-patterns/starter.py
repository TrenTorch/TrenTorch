import numpy as np


def missingness_rate_by_group(x: np.ndarray, groups: np.ndarray) -> dict:
    """
    x: 1D float array, np.nan marks a missing value
    groups: 1D array of labels, same length as x

    Returns:
        A dict {label: fraction of that group's entries that are
        missing} with one key for every label in groups.
    """
    # TODO: Average the missing mask within each group.
    pass


def mean_by_missingness(target: np.ndarray, other: np.ndarray) -> tuple:
    """
    target: 1D float array with some np.nan
    other: 1D float array of the same length, no missing values

    Returns:
        (mean_when_observed, mean_when_missing): the mean of `other`
        over the rows where target is present, and where it is missing.
        An empty side gives nan.
    """
    # TODO: Split the rows of `other` by the missing mask of `target`.
    pass


def likely_mechanism(target: np.ndarray, other: np.ndarray, threshold: float = 0.2) -> str:
    """
    Returns "MAR-like" if the gap between the two means from
    mean_by_missingness, divided by the standard deviation of `other`,
    is at least `threshold`, otherwise "MCAR-like". Also "MCAR-like"
    when nothing is missing or `other` has zero standard deviation.
    """
    # TODO: Compute the standardized gap d from Theory.
    pass


def add_missing_indicators(x: np.ndarray) -> np.ndarray:
    """
    x: 2D float array with some np.nan

    Returns:
        A new array: x unchanged, followed by one 0/1 flag column for
        each column of x that has at least one missing value, in column
        order. x must not be modified.
    """
    # TODO: Stack the flag columns to the right of x.
    pass
