import numpy as np


def confusion_matrix(pred: np.ndarray, target: np.ndarray, n_classes: int) -> np.ndarray:
    """C[true, pred] pixel counts, shape (n_classes, n_classes)."""
    # TODO
    pass


def mean_iou(conf: np.ndarray):
    """Returns (mean IoU ignoring undefined classes, per-class IoU with nan for undefined)."""
    # TODO
    pass
