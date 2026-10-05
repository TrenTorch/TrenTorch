import numpy as np


def sliding_window_accuracy(predictions: np.ndarray, labels: np.ndarray, window_size: int) -> list:
    """
    Splits a long stream of (prediction, true label) pairs into
    consecutive, non-overlapping windows of window_size, and computes
    accuracy WITHIN each window separately -- this is exactly what
    lets a shift in accuracy over time become visible, which a single
    accuracy number computed over the WHOLE stream would completely
    hide (concept drift is about the relationship P(y|x) changing
    partway through, and a single average erases exactly that).
    """
    # TODO: correct = (predictions == labels), as a float array. For i
    # in range(0, len(correct) - window_size + 1, window_size), compute
    # correct[i:i+window_size].mean() and collect those into a list.
    pass


def detect_concept_drift(window_accuracies: list, baseline_accuracy: float, drop_threshold: float) -> bool:
    """
    Flags drift if ANY window's accuracy has fallen more than
    drop_threshold below the established baseline accuracy -- a
    genuine (if simple) drift detector, distinct from
    01-data-drift-psi's INPUT-distribution check: this one watches the
    model's actual PERFORMANCE, which is exactly what changes when the
    input/target RELATIONSHIP shifts even while inputs look unchanged.
    """
    # TODO: return True if any window_accuracy satisfies
    # (baseline_accuracy - window_accuracy) > drop_threshold.
    pass


def first_drift_window(window_accuracies: list, baseline_accuracy: float, drop_threshold: float) -> int | None:
    """
    Returns the INDEX of the first window where drift was detected (by
    the same rule detect_concept_drift uses), or None if drift never
    occurred -- useful for pinpointing roughly WHEN a shift happened,
    not just whether it happened at all.
    """
    # TODO: loop with enumerate over window_accuracies, return the
    # first index where (baseline_accuracy - accuracy) > drop_threshold;
    # return None if the loop finishes without finding one.
    pass
