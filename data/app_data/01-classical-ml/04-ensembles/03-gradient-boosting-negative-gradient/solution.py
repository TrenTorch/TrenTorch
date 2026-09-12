import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).build_regression_tree


def negative_gradient(targets: np.ndarray, predictions: np.ndarray) -> np.ndarray:
    return targets - predictions


def fit_tree_to_negative_gradient(
    input: np.ndarray,
    targets: np.ndarray,
    predictions: np.ndarray,
    max_depth: int,
) -> dict:
    residuals = negative_gradient(targets, predictions)
    return build_regression_tree(input, residuals, max_depth)
