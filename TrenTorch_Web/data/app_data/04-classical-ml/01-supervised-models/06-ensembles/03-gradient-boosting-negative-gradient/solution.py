
import numpy as np

from _load import load_solution

build_regression_tree = load_solution("decision-trees-regression-trees").build_regression_tree


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
