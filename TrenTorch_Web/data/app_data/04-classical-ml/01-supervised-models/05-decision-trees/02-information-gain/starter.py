import numpy as np


def information_gain(
    parent_labels: np.ndarray,
    left_labels: np.ndarray,
    right_labels: np.ndarray,
) -> float:
    """
    parent_labels: labels of every sample in the node before splitting.
    left_labels, right_labels: parent_labels partitioned by the
    candidate split, every sample in exactly one of the two.

    Returns:
        how much the split reduces Gini impurity, a float.
    """
    # TODO: gain = gini_impurity(parent_labels) minus the size-weighted
    # average of gini_impurity(left_labels) and gini_impurity(right_labels).
    pass
