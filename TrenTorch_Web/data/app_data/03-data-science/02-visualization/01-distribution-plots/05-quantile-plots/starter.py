import math

import numpy as np


def normal_ppf(p: float) -> float:
    """
    Returns the standard normal quantile of p (the z with Phi(z) = p),
    accurate to at least 1e-9, for 0 < p < 1.

    Raises:
        ValueError: if p is not strictly between 0 and 1.
    Do not use scipy; math.erf and bisection are enough.
    """
    # TODO: Invert the normal CDF by narrowing an interval.
    pass


def plotting_positions(n: int) -> np.ndarray:
    """Returns the array (i - 0.5) / n for i = 1 .. n."""
    # TODO: Give each sorted value a probability strictly inside (0, 1).
    pass


def qq_points(x: np.ndarray) -> tuple:
    """
    Returns (theoretical, sample): sample is x sorted ascending and
    theoretical[i] = normal_ppf(plotting_positions(n)[i]). Both are 1D
    float arrays of length n.
    """
    # TODO: Pair each sorted value with its normal quantile.
    pass


def qq_line(theoretical: np.ndarray, sample: np.ndarray) -> tuple:
    """
    Returns (slope, intercept) of the line through the points at the
    25th and 75th percentiles of the two arrays:
    slope = (s75 - s25) / (t75 - t25), intercept = s25 - slope * t25.
    """
    # TODO: Draw the line through the quartile points.
    pass


def qq_correlation(x: np.ndarray) -> float:
    """
    Returns the Pearson correlation between theoretical and sample from
    qq_points(x), as a float.
    """
    # TODO: Summarize how straight the plot is.
    pass
