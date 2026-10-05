import numpy as np


def running_total(a: np.ndarray) -> np.ndarray:
    """Cumulative sum of `a`."""
    # TODO: One cumulative operation.
    pass


def cumulative_max(a: np.ndarray) -> np.ndarray:
    """Running maximum: element i is max(a[0..i])."""
    # TODO: Accumulate a maximum.
    pass


def consecutive_differences(a: np.ndarray) -> np.ndarray:
    """a[i+1] - a[i] for every neighbouring pair (length len(a) - 1)."""
    # TODO: Subtract shifted views.
    pass


def percent_change(a: np.ndarray) -> np.ndarray:
    """
    (a[i+1] - a[i]) / a[i] for every neighbouring pair, as a float array of length
    len(a) - 1; NaN where a[i] is 0.
    """
    # TODO: Relative change, guarding against division by zero.
    pass


def moving_average(a: np.ndarray, w: int) -> np.ndarray:
    """
    Mean of every window of `w` consecutive values (length len(a) - w + 1), using
    the cumulative-sum trick, not a Python loop over windows.
    """
    # TODO: Window sums from differences of the cumulative sum.
    pass
