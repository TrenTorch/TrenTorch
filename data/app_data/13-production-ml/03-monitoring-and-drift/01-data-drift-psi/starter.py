import numpy as np


def bin_distribution(samples: np.ndarray, bin_edges: np.ndarray) -> np.ndarray:
    """
    Turns raw samples into a normalized histogram over the given bin
    edges -- a small floor value (1e-6) replaces any empty bin's zero
    count, since a genuinely empty bin would make the PSI formula's
    log(actual/expected) blow up to -infinity otherwise.
    """
    # TODO: counts, _ = np.histogram(samples, bins=bin_edges). Convert
    # to float, replace any zero counts with 1e-6, then normalize by
    # dividing by the total.
    pass


def population_stability_index(expected: np.ndarray, actual: np.ndarray) -> float:
    """
    The Population Stability Index (PSI): a standard, real
    industry metric for how much a distribution has shifted, computed
    as sum((actual - expected) * ln(actual / expected)) across
    matching bins of two ALREADY-NORMALIZED distributions.
    """
    # TODO: float(np.sum((actual - expected) * np.log(actual / expected)))
    pass


def detect_data_drift(psi_value: float, threshold: float = 0.2) -> bool:
    """
    The real, commonly-used PSI interpretation: values below ~0.1
    indicate no meaningful shift, 0.1-0.25 a moderate shift, and above
    ~0.25 a significant one -- this exercise uses a single configurable
    threshold rather than the full three-tier scale.
    """
    # TODO: psi_value > threshold
    pass
