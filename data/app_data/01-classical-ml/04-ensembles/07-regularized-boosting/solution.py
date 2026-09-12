import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

predict_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).predict_regression_tree


def xgboost_leaf_value(gradients: np.ndarray, hessians: np.ndarray, lam: float) -> float:
    return float(-np.sum(gradients) / (np.sum(hessians) + lam))


def xgboost_split_gain(
    gradients: np.ndarray, hessians: np.ndarray, left_mask: np.ndarray, lam: float
) -> float:
    grad_total, hess_total = gradients.sum(), hessians.sum()
    grad_left, hess_left = gradients[left_mask].sum(), hessians[left_mask].sum()
    grad_right, hess_right = gradients[~left_mask].sum(), hessians[~left_mask].sum()
    return 0.5 * (
        (grad_left**2) / (hess_left + lam)
        + (grad_right**2) / (hess_right + lam)
        - (grad_total**2) / (hess_total + lam)
    )


def find_best_regularized_split(
    input: np.ndarray, gradients: np.ndarray, hessians: np.ndarray, lam: float
) -> tuple[int, float, float] | None:
    n_features = input.shape[1]
    best_gain, best_feature, best_threshold = 0.0, None, None
    for feature in range(n_features):
        values = np.unique(input[:, feature])
        if values.size < 2:
            continue
        thresholds = (values[:-1] + values[1:]) / 2
        for threshold in thresholds:
            left_mask = input[:, feature] <= threshold
            gain = xgboost_split_gain(gradients, hessians, left_mask, lam)
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, feature, threshold
    if best_feature is None:
        return None
    return best_feature, float(best_threshold), float(best_gain)


def build_regularized_tree(
    input: np.ndarray,
    gradients: np.ndarray,
    hessians: np.ndarray,
    max_depth: int,
    lam: float,
) -> dict:
    if max_depth == 0 or gradients.size < 2:
        return {"leaf": True, "prediction": xgboost_leaf_value(gradients, hessians, lam)}

    split = find_best_regularized_split(input, gradients, hessians, lam)
    if split is None:
        return {"leaf": True, "prediction": xgboost_leaf_value(gradients, hessians, lam)}

    feature, threshold, _ = split
    left_mask = input[:, feature] <= threshold
    return {
        "leaf": False,
        "feature": feature,
        "threshold": threshold,
        "left": build_regularized_tree(
            input[left_mask], gradients[left_mask], hessians[left_mask], max_depth - 1, lam
        ),
        "right": build_regularized_tree(
            input[~left_mask], gradients[~left_mask], hessians[~left_mask], max_depth - 1, lam
        ),
    }


def train_regularized_boosting(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    learning_rate: float,
    lam: float,
) -> tuple[float, list[dict]]:
    initial_prediction = float(np.mean(targets))
    predictions = np.full(targets.shape[0], initial_prediction)
    hessians = np.ones_like(targets)
    trees = []
    for _ in range(n_trees):
        gradients = predictions - targets
        tree = build_regularized_tree(input, gradients, hessians, max_depth, lam)
        predictions = predictions + learning_rate * predict_regression_tree(tree, input)
        trees.append(tree)
    return initial_prediction, trees


def predict_regularized_boosting(
    initial_prediction: float,
    trees: list[dict],
    learning_rate: float,
    input: np.ndarray,
) -> np.ndarray:
    predictions = np.full(input.shape[0], initial_prediction)
    for tree in trees:
        predictions = predictions + learning_rate * predict_regression_tree(tree, input)
    return predictions
