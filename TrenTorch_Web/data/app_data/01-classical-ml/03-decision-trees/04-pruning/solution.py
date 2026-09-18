import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gini_impurity = load_solution("01-classical-ml/03-decision-trees/01-gini-impurity").gini_impurity
find_best_split = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).find_best_split
predict_tree = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).predict_tree


def _majority_class(labels: np.ndarray, default: int = 0) -> int:
    if labels.size == 0:
        return default
    values, counts = np.unique(labels, return_counts=True)
    return int(values[np.argmax(counts)])


def build_tree_pre_pruned(
    input: np.ndarray,
    labels: np.ndarray,
    max_depth: int,
    min_samples_leaf: int = 1,
) -> dict:
    default = _majority_class(labels)

    if max_depth == 0 or labels.size < 2 or gini_impurity(labels) == 0.0:
        return {"leaf": True, "prediction": default, "default": default}

    split = find_best_split(input, labels)
    if split is None:
        return {"leaf": True, "prediction": default, "default": default}

    feature, threshold, _ = split
    left_mask = input[:, feature] <= threshold
    if left_mask.sum() < min_samples_leaf or (~left_mask).sum() < min_samples_leaf:
        return {"leaf": True, "prediction": default, "default": default}

    return {
        "leaf": False,
        "feature": feature,
        "threshold": threshold,
        "default": default,
        "left": build_tree_pre_pruned(
            input[left_mask], labels[left_mask], max_depth - 1, min_samples_leaf
        ),
        "right": build_tree_pre_pruned(
            input[~left_mask], labels[~left_mask], max_depth - 1, min_samples_leaf
        ),
    }


def prune_tree(tree: dict, input_val: np.ndarray, labels_val: np.ndarray) -> dict:
    if tree["leaf"]:
        return tree

    left_mask = input_val[:, tree["feature"]] <= tree["threshold"]
    candidate = {
        **tree,
        "left": prune_tree(tree["left"], input_val[left_mask], labels_val[left_mask]),
        "right": prune_tree(tree["right"], input_val[~left_mask], labels_val[~left_mask]),
    }

    subtree_predictions = predict_tree(candidate, input_val)
    subtree_error = int(np.sum(subtree_predictions != labels_val))

    leaf_prediction = _majority_class(labels_val, default=tree["default"])
    leaf_error = int(np.sum(leaf_prediction != labels_val))

    if leaf_error <= subtree_error:
        return {"leaf": True, "prediction": leaf_prediction, "default": tree["default"]}
    return candidate
