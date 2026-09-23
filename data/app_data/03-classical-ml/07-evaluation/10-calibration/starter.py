import numpy as np


def reliability_diagram(
    labels: np.ndarray, probabilities: np.ndarray, n_bins: int = 10
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    labels: {0, 1}-valued.
    probabilities: predicted P(class=1), in [0, 1].

    Returns:
        (bin_confidences, bin_accuracies, bin_counts), each shape
        (n_bins,). bin_confidences[i] is the mean predicted probability
        of samples falling in equal-width bin i; bin_accuracies[i] is
        the actual fraction of those samples that were really class 1;
        bin_counts[i] is how many samples fell in that bin (0 for an
        empty bin, whose confidence/accuracy are then meaningless, left
        as 0).
    """
    # TODO: n_bins equal-width bins covering [0, 1]
    # (np.linspace(0, 1, n_bins+1) for the edges). A sample with
    # probability p falls in bin i if edges[i] <= p < edges[i+1],
    # except the LAST bin, which should also include p == 1.0 exactly
    # (edges[i] <= p <= edges[i+1]). For each bin: count the samples,
    # and if non-empty, mean(probabilities in bin) for confidence,
    # mean(labels in bin) for accuracy (the actual positive rate).
    pass


def expected_calibration_error(
    labels: np.ndarray, probabilities: np.ndarray, n_bins: int = 10
) -> float:
    """
    Returns:
        a single number: the sample-count-weighted average gap between
        confidence and accuracy across every bin, 0 for a perfectly
        calibrated model.
    """
    # TODO: reliability_diagram(), then
    # sum over bins of (bin_count / n_total) * |bin_accuracy - bin_confidence|
    pass
