import numpy as np


def importance_estimate(f, p_pdf, q_pdf, draws: np.ndarray) -> float:
    """
    f, p_pdf, q_pdf: vectorized functions of the draws
    draws: 1D array of samples taken from the proposal q

    Returns:
        mean(f(draws) * w) as a float, with w = p_pdf(draws) / q_pdf(draws).
    """
    # TODO: Reweight each draw by p / q and average.
    pass


def self_normalized_estimate(f, p_pdf, q_pdf, draws: np.ndarray) -> float:
    """
    Returns sum(f(draws) * w) / sum(w) as a float, with the same weights
    as importance_estimate. Unchanged if p_pdf is multiplied by any
    positive constant.
    """
    # TODO: Divide the weighted sum by the sum of the weights.
    pass


def effective_sample_size(weights: np.ndarray) -> float:
    """
    weights: 1D array of non-negative weights, at least one positive

    Returns sum(weights) ** 2 / sum(weights ** 2) as a float.
    """
    # TODO: Measure how evenly the weight is spread.
    pass
