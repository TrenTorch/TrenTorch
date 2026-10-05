import numpy as np


def expected_improvement(
    mean: np.ndarray, std: np.ndarray, best_so_far: float, xi: float = 0.01
) -> np.ndarray:
    """
    mean, std: shape (n_candidates,), a GP's posterior mean and standard
    deviation at every candidate point.
    best_so_far: the best (highest) target value observed so far.
    xi: a small exploration margin.

    Returns:
        shape (n_candidates,): the Expected Improvement acquisition
        value at each candidate. 0 wherever std is 0 (no uncertainty,
        nothing to be gained by exploring there).
    """
    # TODO: improvement = mean - best_so_far - xi
    # z = improvement / std (0 where std is 0, to avoid dividing by zero)
    # normal_pdf(z) = (1/sqrt(2*pi)) * exp(-z^2/2)
    # normal_cdf(z) = 0.5 * (1 + erf(z / sqrt(2)))  -- from math import erf,
    #   np.vectorize it to apply elementwise over an array
    # ei = improvement * normal_cdf(z) + std * normal_pdf(z), except 0
    #   wherever std is 0
    pass


def propose_next_point(
    input_train: np.ndarray,
    targets_train: np.ndarray,
    candidates: np.ndarray,
    length_scale: float,
    variance: float,
    noise: float,
    xi: float = 0.01,
) -> int:
    """
    Returns:
        the index into candidates with the highest Expected Improvement,
        the point Bayesian optimization would evaluate next.
    """
    # TODO: gp_predict() (05-gaussian-processes) on candidates using
    # the current (input_train, targets_train), giving a posterior mean
    # and variance per candidate. std = sqrt(variance). Score every
    # candidate with expected_improvement() against
    # best_so_far=targets_train.max(), return the argmax index.
    pass
