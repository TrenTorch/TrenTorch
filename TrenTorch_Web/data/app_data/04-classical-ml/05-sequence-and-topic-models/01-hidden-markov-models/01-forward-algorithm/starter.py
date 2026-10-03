import numpy as np


def forward_likelihood(pi: np.ndarray, A: np.ndarray, B: np.ndarray, obs) -> float:
    """
    p(obs) for an HMM with initial pi (K,), transitions A (K, K), emissions B (K, M).
    Raise ValueError for non-stochastic inputs, out-of-range observations,
    empty sequences, or shape mismatches.
    """
    pass
