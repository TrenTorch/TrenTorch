import numpy as np


def precision_recall_f1(p: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Precision, recall, and F1 for binary predictions p against labels y.

    p, y: shape (n,), each entry 0 or 1.

    precision = TP / (TP + FP), recall = TP / (TP + FN),
    f1 = 2 * precision * recall / (precision + recall).

    If a denominator is 0 (no predicted positives for precision, no actual
    positives for recall), report 0.0 for that metric instead of crashing.
    """
    # TODO: count tp/fp/fn first, then apply the zero-denominator convention
    # to precision and recall before computing f1.
    pass
