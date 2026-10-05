import numpy as np


def fractional_split_gain(x: np.ndarray, y: np.ndarray, threshold: float) -> tuple[float, float]:
    """
    C4.5-style gain for the split x <= threshold when x may contain NaN.
    Returns (gain, p_left). Raise ValueError for mismatched shapes or all-NaN x.
    """
    pass
