import numpy as np


def smooth_labels(one_hot: np.ndarray, smoothing: float, num_classes: int) -> np.ndarray:
    return one_hot * (1.0 - smoothing) + smoothing / num_classes
