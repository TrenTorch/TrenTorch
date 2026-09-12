import numpy as np


def bernoulli_nb_fit(input: np.ndarray, labels: np.ndarray, alpha: float = 1.0) -> dict:
    """
    input:  shape (n_samples, n_features), every entry 0 or 1.
    alpha:  Laplace (additive) smoothing strength.

    Returns a dict: {"classes": ..., "log_priors": {class: log P(class)},
    "feature_probs": {class: array of P(feature=1 | class), shape (n_features,)}}.
    """
    # TODO: For each distinct class c:
    #   log_priors[c] = log(count of class c / n_samples)
    #   feature_probs[c] = (sum of feature=1 counts within class c + alpha)
    #                          / (count of class c + 2*alpha)
    pass


def bernoulli_log_likelihood(x: np.ndarray, feature_probs: np.ndarray) -> float:
    """
    x: shape (n_features,), a single sample's binary features.
    feature_probs: shape (n_features,), P(feature=1 | class) for one class.

    Returns:
        log P(x | class), assuming every feature is an independent
        Bernoulli variable (Naive Bayes's independence assumption).
    """
    # TODO: sum over features of x*log(p) + (1-x)*log(1-p).
    pass


def bernoulli_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    """
    Returns:
        shape (n_queries,): argmax over classes of
        log_prior[c] + bernoulli_log_likelihood(query, feature_probs[c]).
    """
    # TODO: For each query, score every class by its log prior plus the
    # log-likelihood of that query's features under that class, then
    # pick the class with the highest score.
    pass
