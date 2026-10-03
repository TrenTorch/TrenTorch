import numpy as np


def viterbi(pi: np.ndarray, A: np.ndarray, B: np.ndarray, obs):
    """
    Most likely state path for an HMM. Returns (path, prob) where path is a list
    of T state indices and prob is p(path, obs). Raise ValueError for
    non-stochastic inputs, out-of-range observations, or an empty sequence.
    """
    pass
