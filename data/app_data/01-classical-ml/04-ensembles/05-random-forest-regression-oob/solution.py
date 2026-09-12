import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).build_regression_tree
predict_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).predict_regression_tree


def bootstrap_sample_with_oob(
    input: np.ndarray, targets: np.ndarray, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_samples = input.shape[0]
    indices = rng.integers(0, n_samples, size=n_samples)
    in_bag = np.zeros(n_samples, dtype=bool)
    in_bag[indices] = True
    oob_indices = np.where(~in_bag)[0]
    return input[indices], targets[indices], oob_indices


def train_random_forest_regressor(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    seed: int | None = None,
) -> list[tuple[dict, np.ndarray]]:
    rng = np.random.default_rng(seed)
    forest = []
    for _ in range(n_trees):
        boot_input, boot_targets, oob_indices = bootstrap_sample_with_oob(input, targets, seed=rng)
        tree = build_regression_tree(boot_input, boot_targets, max_depth)
        forest.append((tree, oob_indices))
    return forest


def predict_random_forest_regressor(
    forest: list[tuple[dict, np.ndarray]], input: np.ndarray
) -> np.ndarray:
    predictions = np.array([predict_regression_tree(tree, input) for tree, _ in forest])
    return predictions.mean(axis=0)


def oob_error(forest: list[tuple[dict, np.ndarray]], input: np.ndarray, targets: np.ndarray) -> float:
    n_samples = input.shape[0]
    oob_sums = np.zeros(n_samples)
    oob_counts = np.zeros(n_samples)
    for tree, oob_indices in forest:
        if oob_indices.size == 0:
            continue
        oob_sums[oob_indices] += predict_regression_tree(tree, input[oob_indices])
        oob_counts[oob_indices] += 1

    has_oob_prediction = oob_counts > 0
    oob_predictions = oob_sums[has_oob_prediction] / oob_counts[has_oob_prediction]
    oob_targets = targets[has_oob_prediction]
    return float(np.mean((oob_predictions - oob_targets) ** 2))
