import numpy as np


def feature_importances(
    tree: dict,
    input: np.ndarray,
    labels: np.ndarray,
    n_features: int,
) -> np.ndarray:
    """
    tree: a tree from build_tree (03-best-split-minimal-tree), fitted
    on (input, labels).
    input, labels: the exact data the tree was built from.
    n_features: input.shape[1], the total number of features.

    Returns:
        shape (n_features,), each entry the total sample-weighted
        information gain attributed to splits on that feature,
        normalized to sum to 1. All zeros if the tree is a single leaf.
    """
    # TODO: Walk the tree from the root, re-partitioning input/labels
    # at every split node the same way build_tree did (using the
    # node's own stored feature/threshold). At each split node, compute
    # information_gain() for that split and add
    # (node_labels.size / total_samples) * gain to importances[feature].
    # Recurse into both children with their partitioned subsets.
    # Normalize the final array to sum to 1 (skip normalizing if the
    # total is 0, to avoid dividing by zero).
    pass
