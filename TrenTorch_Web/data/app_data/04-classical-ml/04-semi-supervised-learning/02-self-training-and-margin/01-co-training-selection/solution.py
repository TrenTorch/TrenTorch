import numpy as np


def pick_pseudo_labels(
    conf_a: np.ndarray,
    pred_a: np.ndarray,
    conf_b: np.ndarray,
    pred_b: np.ndarray,
    threshold: float,
):
    conf_a = np.asarray(conf_a, dtype=float)
    conf_b = np.asarray(conf_b, dtype=float)
    pred_a = np.asarray(pred_a)
    pred_b = np.asarray(pred_b)
    n = conf_a.shape[0]
    if any(arr.shape != (n,) for arr in (conf_b, pred_a, pred_b)):
        raise ValueError("all four inputs must be 1-D with the same length")
    if not (0.0 < threshold <= 1.0):
        raise ValueError("threshold must lie in (0, 1]")
    if np.any((conf_a < 0) | (conf_a > 1) | (conf_b < 0) | (conf_b > 1)):
        raise ValueError("confidences must lie in [0, 1]")
    sure_a = conf_a >= threshold
    sure_b = conf_b >= threshold
    agree = pred_a == pred_b
    keep = sure_a | sure_b
    keep &= ~(sure_a & sure_b & ~agree)
    indices = np.flatnonzero(keep)
    labels = np.where(sure_a[indices], pred_a[indices], pred_b[indices])
    return indices, labels
