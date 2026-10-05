import numpy as np


def pick_pseudo_labels(
    conf_a: np.ndarray,
    pred_a: np.ndarray,
    conf_b: np.ndarray,
    pred_b: np.ndarray,
    threshold: float,
):
    """
    Return (indices, labels) for points where at least one view has confidence
    >= threshold. Skip points where both views are confident and disagree.
    Raise ValueError for length mismatches, invalid threshold, or confidences
    outside [0, 1].
    """
    pass
