import numpy as np


def smooth_labels(one_hot: np.ndarray, smoothing: float, num_classes: int) -> np.ndarray:
    """
    Softens a one-hot target vector: instead of putting all probability
    mass (1.0) on the true class and 0.0 everywhere else, spreads a small
    amount of mass (`smoothing`) evenly across ALL classes, including the
    true one.
    """
    pass
