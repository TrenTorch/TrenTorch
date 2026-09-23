import numpy as np


def gaussian_nb_fit(input: np.ndarray, labels: np.ndarray, var_smoothing: float = 1e-9) -> dict:
    """
    input: shape (n_samples, n_features), real-valued this time (not
    binary, that was 02-naive-bayes-bernoulli).

    Returns a dict: {"classes": ..., "log_priors": {class: log P(class)},
    "means": {class: array (n_features,)}, "variances": {class: array (n_features,)}}.

    var_smoothing: a small fraction of the largest feature variance
    across the WHOLE dataset, added to every class's per-feature
    variance, so a feature that's exactly constant within some class
    never gets a variance of literal 0.
    """
    # TODO: epsilon = var_smoothing * np.var(input, axis=0).max()
    # For each distinct class c:
    #   log_priors[c] = log(count of class c / n_samples)
    #   means[c] = mean of that class's rows, per feature
    #   variances[c] = variance of that class's rows, per feature, + epsilon
    pass


def gaussian_log_likelihood(x: np.ndarray, mean: np.ndarray, variance: np.ndarray) -> float:
    """
    x, mean, variance: shape (n_features,).

    Returns:
        log P(x | class), assuming every feature is an independent
        Gaussian given the class (Naive Bayes's independence
        assumption, applied to continuous features this time).
    """
    # TODO: sum over features of the Gaussian log-density:
    # -0.5*log(2*pi*variance) - (x-mean)^2 / (2*variance)
    pass


def gaussian_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    """Same scoring/argmax pattern as 02-naive-bayes-bernoulli's bernoulli_nb_predict."""
    # TODO: For each query, score every class by log_prior +
    # gaussian_log_likelihood(query, means[c], variances[c]), pick the
    # class with the highest score.
    pass
