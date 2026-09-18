import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gini_impurity = load_solution("01-classical-ml/03-decision-trees/01-gini-impurity").gini_impurity
information_gain = load_solution(
    "01-classical-ml/03-decision-trees/02-information-gain"
).information_gain


def _majority_class(labels: np.ndarray) -> int:
    values, counts = np.unique(labels, return_counts=True)
    return int(values[np.argmax(counts)])


def find_best_split(input: np.ndarray, labels: np.ndarray) -> tuple[int, float, float] | None:
    n_features = input.shape[1]
    best_gain, best_feature, best_threshold = 0.0, None, None
    for feature in range(n_features):
        values = np.unique(input[:, feature])
        if values.size < 2:
            continue
        # Midpoint between two adjacent present values: every sample
        # <= the lower value lands left, every sample >= the higher
        # value lands right, so both sides are guaranteed non-empty.
        thresholds = (values[:-1] + values[1:]) / 2
        for threshold in thresholds:
            left_mask = input[:, feature] <= threshold
            gain = information_gain(labels, labels[left_mask], labels[~left_mask])
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, feature, threshold
    if best_feature is None:
        return None
    return best_feature, float(best_threshold), float(best_gain)


def build_tree(input: np.ndarray, labels: np.ndarray, max_depth: int) -> dict:
    if max_depth == 0 or labels.size < 2 or gini_impurity(labels) == 0.0:
        return {"leaf": True, "prediction": _majority_class(labels)}

    split = find_best_split(input, labels)
    if split is None:
        return {"leaf": True, "prediction": _majority_class(labels)}

    feature, threshold, _ = split
    left_mask = input[:, feature] <= threshold
    return {
        "leaf": False,
        "feature": feature,
        "threshold": threshold,
        "left": build_tree(input[left_mask], labels[left_mask], max_depth - 1),
        "right": build_tree(input[~left_mask], labels[~left_mask], max_depth - 1),
    }


def predict_tree(tree: dict, input: np.ndarray) -> np.ndarray:
    predictions = np.empty(input.shape[0], dtype=int)
    for i in range(input.shape[0]):
        node = tree
        while not node["leaf"]:
            if input[i, node["feature"]] <= node["threshold"]:
                node = node["left"]
            else:
                node = node["right"]
        predictions[i] = node["prediction"]
    return predictions
