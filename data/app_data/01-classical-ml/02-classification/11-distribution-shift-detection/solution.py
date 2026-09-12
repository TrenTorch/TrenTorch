import numpy as np

_EPS = 1e-6


def bin_proportions(values: np.ndarray, bin_edges: np.ndarray) -> np.ndarray:
    counts, _ = np.histogram(values, bins=bin_edges)
    return counts / len(values)


def population_stability_index(
    train_values: np.ndarray, live_values: np.ndarray, num_bins: int = 10
) -> float:
    bin_edges = np.quantile(train_values, np.linspace(0.0, 1.0, num_bins + 1))
    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf

    train_proportions = np.clip(bin_proportions(train_values, bin_edges), _EPS, 1.0)
    live_proportions = np.clip(bin_proportions(live_values, bin_edges), _EPS, 1.0)

    return float(np.sum((live_proportions - train_proportions) * np.log(live_proportions / train_proportions)))


def detect_distribution_shift(
    train_values: np.ndarray, live_values: np.ndarray, num_bins: int = 10, threshold: float = 0.2
) -> bool:
    return population_stability_index(train_values, live_values, num_bins) > threshold
