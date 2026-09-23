import numpy as np


def radius_feature(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Distance from the origin, given two raw coordinate features.
    See Theory for why this single derived number can be dramatically
    more informative than x and y individually.
    """
    pass


def ratio_feature(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    """
    A derived feature combining two raw ones into a single, often more
    meaningful quantity (e.g. price / area = price-per-square-foot).
    """
    pass
