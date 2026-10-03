import numpy as np


def five_number_summary(x: np.ndarray) -> tuple:
    """
    Returns (minimum, q1, median, q3, maximum) as floats, with quartiles
    from np.percentile's default linear interpolation.
    """
    # TODO: Take the extremes and the three quartiles.
    pass


def box_plot_stats(x: np.ndarray, whisker: float = 1.5) -> dict:
    """
    Returns a dict with keys "q1", "median", "q3", "lower_whisker",
    "upper_whisker" and "outliers". The fences are q1 - whisker * IQR and
    q3 + whisker * IQR. Each whisker ends at the most extreme value of x
    that is inside its fence (inclusive), and "outliers" is a sorted
    array of the values outside the fences.
    """
    # TODO: Build the fences, then split the data into inside and outside.
    pass
