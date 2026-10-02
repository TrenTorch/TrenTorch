import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution

normal_pdf = load_solution("02-mathematics/04-statistics/01-probability/13-likelihood-vs-probability").normal_pdf


def negative_log_likelihood_normal(x: np.ndarray, mean: float, std: float) -> float:
    return float(-np.sum(np.log(normal_pdf(x, mean, std))))


def mle_normal_mean(x: np.ndarray) -> float:
    return float(np.mean(x))


def mle_normal_std(x: np.ndarray) -> float:
    mean = mle_normal_mean(x)
    return float(np.sqrt(np.mean((x - mean) ** 2)))
