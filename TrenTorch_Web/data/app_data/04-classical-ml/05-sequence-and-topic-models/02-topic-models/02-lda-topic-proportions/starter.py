import numpy as np


def lda_estimates(doc_topic: np.ndarray, topic_word: np.ndarray, alpha: float, beta: float):
    """
    Returns (theta, phi): theta (D, K) document-topic mixtures and phi (K, V)
    topic-word distributions, both smoothed by the Dirichlet priors.
    Raise ValueError for shape mismatches, nonpositive priors, or negative counts.
    """
    pass
