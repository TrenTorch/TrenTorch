import numpy as np


def extra_tree_split(x: np.ndarray, y: np.ndarray, seed: int):
    """
    Extremely randomized split on one feature. Draws a uniform threshold
    between min and max of x and returns (threshold, gini_gain). Returns
    (None, 0.0) when x is constant. Raises ValueError on length mismatch.
    """
    pass
