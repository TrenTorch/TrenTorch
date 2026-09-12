import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

normal_pdf = load_solution("00-math-and-statistics/03-probability/06-likelihood-vs-probability").normal_pdf
negative_log_likelihood_normal = load_solution(
    "00-math-and-statistics/03-probability/07-maximum-likelihood-estimation"
).negative_log_likelihood_normal


def negative_log_posterior_normal(
    mean_candidate: float, x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    """
    -log(posterior) up to a constant, for a Normal likelihood (data_std
    assumed known) with a Normal prior on the mean:

        -log(posterior) = -log(likelihood) + -log(prior) + constant

    (Bayes' theorem's denominator, P(evidence), doesn't depend on
    mean_candidate, so it's a constant here and can be dropped when
    all you want is the ARGMIN over mean_candidate.)

    negative_log_likelihood_normal and normal_pdf are already provided
    above.
    """
    pass


def map_estimate_normal_mean(
    x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    """
    The closed-form MAP estimate for a Normal mean with a Normal prior:
    a precision-weighted average of the sample mean and the prior mean.
    See Theory for the exact formula and derivation sketch.
    """
    pass
