import numpy as np


def reliability_diagram(
    labels: np.ndarray, probabilities: np.ndarray, n_bins: int = 10
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_confidences = np.zeros(n_bins)
    bin_accuracies = np.zeros(n_bins)
    bin_counts = np.zeros(n_bins, dtype=int)

    for i in range(n_bins):
        lower, upper = bin_edges[i], bin_edges[i + 1]
        if i == n_bins - 1:
            in_bin = (probabilities >= lower) & (probabilities <= upper)
        else:
            in_bin = (probabilities >= lower) & (probabilities < upper)

        bin_counts[i] = in_bin.sum()
        if bin_counts[i] > 0:
            bin_confidences[i] = probabilities[in_bin].mean()
            bin_accuracies[i] = labels[in_bin].mean()

    return bin_confidences, bin_accuracies, bin_counts


def expected_calibration_error(
    labels: np.ndarray, probabilities: np.ndarray, n_bins: int = 10
) -> float:
    bin_confidences, bin_accuracies, bin_counts = reliability_diagram(labels, probabilities, n_bins)
    n_total = probabilities.shape[0]
    weights = bin_counts / n_total
    return float(np.sum(weights * np.abs(bin_accuracies - bin_confidences)))
