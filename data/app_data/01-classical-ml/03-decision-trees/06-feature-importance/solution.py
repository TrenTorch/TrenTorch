import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

information_gain = load_solution(
    "01-classical-ml/03-decision-trees/02-information-gain"
).information_gain


def feature_importances(
    tree: dict,
    input: np.ndarray,
    labels: np.ndarray,
    n_features: int,
) -> np.ndarray:
    importances = np.zeros(n_features)
    total_samples = labels.size

    def walk(node: dict, node_input: np.ndarray, node_labels: np.ndarray) -> None:
        if node["leaf"]:
            return
        feature = node["feature"]
        left_mask = node_input[:, feature] <= node["threshold"]
        left_labels, right_labels = node_labels[left_mask], node_labels[~left_mask]
        gain = information_gain(node_labels, left_labels, right_labels)
        weight = node_labels.size / total_samples
        importances[feature] += weight * gain
        walk(node["left"], node_input[left_mask], left_labels)
        walk(node["right"], node_input[~left_mask], right_labels)

    walk(tree, input, labels)

    total = importances.sum()
    if total > 0:
        importances = importances / total
    return importances
