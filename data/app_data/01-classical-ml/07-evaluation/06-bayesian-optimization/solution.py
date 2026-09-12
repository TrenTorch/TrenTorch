import sys
from math import erf
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gp_predict = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/05-gaussian-processes"
).gp_predict

_normal_cdf = np.vectorize(lambda z: 0.5 * (1.0 + erf(z / np.sqrt(2.0))))


def expected_improvement(
    mean: np.ndarray, std: np.ndarray, best_so_far: float, xi: float = 0.01
) -> np.ndarray:
    improvement = mean - best_so_far - xi
    with np.errstate(divide="ignore", invalid="ignore"):
        z = np.where(std > 0, improvement / std, 0.0)
    normal_pdf = (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-(z**2) / 2.0)
    ei = improvement * _normal_cdf(z) + std * normal_pdf
    return np.where(std > 0, ei, 0.0)


def propose_next_point(
    input_train: np.ndarray,
    targets_train: np.ndarray,
    candidates: np.ndarray,
    length_scale: float,
    variance: float,
    noise: float,
    xi: float = 0.01,
) -> int:
    mean, gp_variance = gp_predict(input_train, targets_train, candidates, length_scale, variance, noise)
    std = np.sqrt(gp_variance)
    ei = expected_improvement(mean, std, best_so_far=targets_train.max(), xi=xi)
    return int(np.argmax(ei))
