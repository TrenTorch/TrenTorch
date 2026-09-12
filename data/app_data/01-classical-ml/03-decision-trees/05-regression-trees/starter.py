import numpy as np


def variance(targets: np.ndarray) -> float:
    """Population variance of targets. Empty input has variance 0.0 by convention."""
    # TODO: np.var handles this in one call -- just guard the empty case.
    pass


def variance_reduction(
    parent_targets: np.ndarray,
    left_targets: np.ndarray,
    right_targets: np.ndarray,
) -> float:
    """Same shape as information_gain, with variance in place of Gini impurity."""
    # TODO: parent variance minus the size-weighted average of the two
    # children's variances.
    pass


def find_best_regression_split(
    input: np.ndarray, targets: np.ndarray
) -> tuple[int, float, float] | None:
    """Same search as find_best_split, scored by variance_reduction instead of information_gain."""
    # TODO: For each feature, try every midpoint-between-consecutive-
    # unique-values threshold. Track the best (feature, threshold,
    # reduction) seen.
    pass


def build_regression_tree(input: np.ndarray, targets: np.ndarray, max_depth: int) -> dict:
    """
    Same recursive structure as build_tree, for regression:
      leaf node:  {"leaf": True, "prediction": <mean of this node's targets>}
      split node: {"leaf": False, "feature": i, "threshold": t, "left": ..., "right": ...}

    Stop at a leaf when max_depth reaches 0, fewer than 2 samples
    remain, every target in this node is already identical (variance
    0), or find_best_regression_split finds nothing.
    """
    # TODO: Base case -> leaf with prediction = mean(targets).
    # Otherwise: find_best_regression_split(), then recurse on each
    # side with max_depth - 1.
    pass


def predict_regression_tree(tree: dict, input: np.ndarray) -> np.ndarray:
    """Same traversal as predict_tree, returning float predictions instead of class labels."""
    # TODO: For each row, walk from the root to a leaf the same way
    # predict_tree does, and record that leaf's prediction.
    pass
