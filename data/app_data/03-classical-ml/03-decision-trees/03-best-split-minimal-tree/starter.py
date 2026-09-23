import numpy as np


def find_best_split(input: np.ndarray, labels: np.ndarray) -> tuple[int, float, float] | None:
    """
    input:  shape (n_samples, n_features)
    labels: shape (n_samples,)

    Searches every feature and every candidate threshold (the midpoint
    between each pair of consecutive sorted unique values of that
    feature) for the split "feature <= threshold vs. feature >
    threshold" that maximizes information_gain.

    Returns:
        (feature_index, threshold, gain) for the best split found, or
        None if no split improves on the parent's impurity at all.
    """
    # TODO: For each feature, try every midpoint-between-consecutive-
    # unique-values threshold (guaranteed to put at least one sample on
    # each side). Track the best (feature, threshold, gain) seen, using
    # information_gain() and the node's true labels on each side.
    pass


def build_tree(input: np.ndarray, labels: np.ndarray, max_depth: int) -> dict:
    """
    Recursively builds a decision tree using find_best_split() at every
    node.

    Returns a tree as nested dicts:
      leaf node:  {"leaf": True, "prediction": <majority class, int>}
      split node: {"leaf": False, "feature": <int>, "threshold": <float>,
                   "left": <subtree>, "right": <subtree>}

    Stop and return a leaf when: max_depth reaches 0, fewer than 2
    samples remain, the node is already pure, or find_best_split()
    finds no split that improves on the parent at all.
    """
    # TODO: Base case -> leaf with the majority class.
    # Otherwise: find_best_split(), then recurse on each side with
    # max_depth - 1, and assemble the split node.
    pass


def predict_tree(tree: dict, input: np.ndarray) -> np.ndarray:
    """
    input: shape (n_samples, n_features)

    Returns:
        shape (n_samples,), the predicted class for each row, found by
        walking the tree from the root to a leaf.
    """
    # TODO: For each row, walk from the root: at a split node, go left
    # if input[i, feature] <= threshold, else right. Stop at a leaf and
    # record its prediction.
    pass
