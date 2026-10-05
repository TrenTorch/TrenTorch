import numpy as np


def replace_where(a: np.ndarray, mask: np.ndarray, value) -> np.ndarray:
    """A copy of `a` with `value` at the positions where boolean `mask` is True."""
    # TODO: Do not change the input.
    pass


def clip_to_percentiles(a: np.ndarray, low: float, high: float) -> np.ndarray:
    """
    Clip every value of `a` into [P_low, P_high], where P_q is the q-th percentile of
    `a` (np.percentile, linear interpolation). Returns a new array.
    """
    # TODO: Find the two limits from the data, then clip.
    pass


def sign_class(a: np.ndarray) -> np.ndarray:
    """-1 where a < 0, 0 where a == 0, 1 where a > 0 (integer array), using np.select."""
    # TODO: Several conditions, first match wins.
    pass


def bucket_label(a: np.ndarray, low: float, high: float) -> np.ndarray:
    """Array of the strings 'low' (a < low), 'high' (a >= high), otherwise 'mid'."""
    # TODO: Choose a label per element.
    pass
