import numpy as np


def bin_distribution(samples: np.ndarray, bin_edges: np.ndarray) -> np.ndarray:
    counts, _ = np.histogram(samples, bins=bin_edges)
    counts = counts.astype(float)
    counts[counts == 0] = 1e-6
    return counts / counts.sum()


def population_stability_index(expected: np.ndarray, actual: np.ndarray) -> float:
    return float(np.sum((actual - expected) * np.log(actual / expected)))


def detect_data_drift(psi_value: float, threshold: float = 0.2) -> bool:
    return psi_value > threshold
