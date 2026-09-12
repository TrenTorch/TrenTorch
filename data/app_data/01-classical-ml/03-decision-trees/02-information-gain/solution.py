import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gini_impurity = load_solution("01-classical-ml/03-decision-trees/01-gini-impurity").gini_impurity


def information_gain(
    parent_labels: np.ndarray,
    left_labels: np.ndarray,
    right_labels: np.ndarray,
) -> float:
    n_samples = parent_labels.size
    weighted_child_impurity = (left_labels.size / n_samples) * gini_impurity(left_labels) + (
        right_labels.size / n_samples
    ) * gini_impurity(right_labels)
    return gini_impurity(parent_labels) - weighted_child_impurity
