
import numpy as np

from _load import load_solution

gini_impurity = load_solution("decision-trees-gini-impurity").gini_impurity


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
