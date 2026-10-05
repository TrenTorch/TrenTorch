import numpy as np


def gmm_log_likelihood(
    input: np.ndarray, weights: np.ndarray, means: np.ndarray, variances: np.ndarray
) -> float:
    """
    Returns:
        the total log-likelihood of input under the current mixture:
        sum over samples of log( sum over components of
        weight[j] * P(x_i | component j) ).
    """
    # TODO: Same log_probs[i,j] = log(weights[j]) + gaussian_log_likelihood(...)
    # matrix as gmm_e_step. This time, instead of normalizing each row
    # into responsibilities, sum each row in a numerically stable way
    # (log-sum-exp: subtract the row max, exponentiate, sum, take log,
    # add the max back), then sum those per-sample values across all
    # samples.
    pass


def fit_gmm(input: np.ndarray, n_components: int, max_iter: int, seed: int | None = None) -> dict:
    """
    Assembles 04-gaussian-mixture's gmm_e_step/gmm_m_step into the full
    EM training loop.

    Returns a dict: {"weights", "means", "variances", "responsibilities"
    (from the LAST E-step), "log_likelihood_history" (array, one entry
    per iteration, after that iteration's M-step)}.
    """
    # TODO: Initialize: pick n_components distinct random rows of input
    # (rng.choice without replacement) as the initial means, uniform
    # weights (1/n_components each), variances = the overall per-feature
    # variance of input, tiled for every component.
    # Repeat max_iter times: E-step, M-step, then record
    # gmm_log_likelihood() of the just-updated parameters.
    pass
