import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

predict_tree = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).predict_tree


def random_forest_predict(trees: list[dict], input: np.ndarray) -> np.ndarray:
    votes = np.array([predict_tree(tree, input) for tree in trees])  # (n_trees, n_samples)
    predictions = np.empty(input.shape[0], dtype=int)
    for i in range(input.shape[0]):
        values, counts = np.unique(votes[:, i], return_counts=True)
        predictions[i] = values[np.argmax(counts)]
    return predictions
