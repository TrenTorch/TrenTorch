import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

fit_tree_to_negative_gradient = load_solution(
    "01-classical-ml/04-ensembles/03-gradient-boosting-negative-gradient"
).fit_tree_to_negative_gradient
predict_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).predict_regression_tree


def train_gradient_boosting(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    learning_rate: float,
) -> tuple[float, list[dict]]:
    initial_prediction = float(np.mean(targets))
    predictions = np.full(targets.shape[0], initial_prediction)
    trees = []
    for _ in range(n_trees):
        tree = fit_tree_to_negative_gradient(input, targets, predictions, max_depth)
        predictions = predictions + learning_rate * predict_regression_tree(tree, input)
        trees.append(tree)
    return initial_prediction, trees


def predict_gradient_boosting(
    initial_prediction: float,
    trees: list[dict],
    learning_rate: float,
    input: np.ndarray,
) -> np.ndarray:
    predictions = np.full(input.shape[0], initial_prediction)
    for tree in trees:
        predictions = predictions + learning_rate * predict_regression_tree(tree, input)
    return predictions
