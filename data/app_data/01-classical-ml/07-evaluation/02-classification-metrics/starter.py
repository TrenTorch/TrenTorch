import numpy as np


def precision_recall_f1(
    labels: np.ndarray, predictions: np.ndarray
) -> tuple[float, float, float]:
    """
    labels, predictions: {0, 1}-valued, same shape.

    Returns:
        (precision, recall, f1). Each is 0.0 if its denominator would
        be 0 (no positive predictions for precision, no actual
        positives for recall).
    """
    # TODO: true_positives  = predicted 1 AND actually 1
    #       false_positives = predicted 1 AND actually 0
    #       false_negatives = predicted 0 AND actually 1
    # precision = tp / (tp + fp), recall = tp / (tp + fn)
    # f1 = 2 * precision * recall / (precision + recall)
    pass


def roc_curve(labels: np.ndarray, scores: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    labels: {0, 1}-valued.
    scores: a continuous score (e.g. a predicted probability), higher
    means "more likely class 1."

    Returns:
        (fpr, tpr, thresholds), one entry per threshold tried:
        every distinct score value, from highest to lowest, plus
        +infinity (the threshold that classifies everything as 0).
        fpr[i]/tpr[i] are the false/true positive rate when predicting
        1 for every score >= thresholds[i].
    """
    # TODO: thresholds = [inf] followed by every unique score, sorted
    # descending. For each threshold, predictions = (scores >=
    # threshold), then the same tp/fp counting as precision_recall_f1,
    # divided by the TOTAL number of actual positives/negatives (not
    # predicted) to get tpr/fpr.
    pass


def auc(fpr: np.ndarray, tpr: np.ndarray) -> float:
    """Area under the ROC curve, via the trapezoidal rule."""
    # TODO: Sort by fpr first (roc_curve's own order is descending by
    # threshold, not ascending by fpr), then np.trapezoid.
    pass
