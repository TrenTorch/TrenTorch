from typing import Callable

import numpy as np


def f1_metric(labels: np.ndarray, predictions: np.ndarray) -> float:
    """F1 score, via 02-classification-metrics's precision_recall_f1. The default metric_fn."""
    # TODO: one line, call precision_recall_f1 and return the third value.
    pass


def optimize_threshold(
    labels: np.ndarray,
    scores: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float] = f1_metric,
) -> tuple[float, float]:
    """
    Tries every distinct score value as a decision threshold, scoring
    (scores >= threshold) predictions with metric_fn each time.

    Returns:
        (best_threshold, best_score): the threshold that maximizes
        metric_fn, and the score it achieved.
    """
    # TODO: For every unique score value, form predictions =
    # (scores >= threshold), score them with metric_fn(labels,
    # predictions), track the threshold with the highest score.
    pass
