import numpy as np


def state_posteriors(pi: np.ndarray, A: np.ndarray, B: np.ndarray, obs) -> np.ndarray:
    """
    Smoothed posteriors gamma[t, i] = p(s_t = i | obs) via forward-backward.
    Returns a (T, K) array with rows summing to 1. Raise ValueError for
    non-stochastic inputs, out-of-range observations, or an empty sequence.
    """
    pass
