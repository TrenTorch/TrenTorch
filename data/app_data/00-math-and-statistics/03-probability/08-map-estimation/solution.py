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
    nll = negative_log_likelihood_normal(x, mean_candidate, data_std)
    neg_log_prior = float(-np.log(normal_pdf(np.array([mean_candidate]), prior_mean, prior_std))[0])
    return nll + neg_log_prior


def map_estimate_normal_mean(
    x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    n = len(x)
    sample_mean = np.mean(x)
    data_precision = n / data_std**2
    prior_precision = 1.0 / prior_std**2
    return float(
        (data_precision * sample_mean + prior_precision * prior_mean)
        / (data_precision + prior_precision)
    )
