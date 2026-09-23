import numpy as np


def build_isolation_tree(input: np.ndarray, max_depth: int, rng: np.random.Generator) -> dict:
    """
    Builds one isolation tree: at each node, pick a random feature and a
    random threshold uniformly between that feature's min and max among
    the samples reaching this node, then split on it. No label, no
    impurity criterion, purely random.

    Returns a tree as nested dicts:
      leaf node:  {"leaf": True, "size": <number of samples at this leaf>}
      split node: {"leaf": False, "feature": i, "threshold": t, "left": ..., "right": ...}
    """
    # TODO: Base case -> leaf, if max_depth == 0, or 1 or fewer samples
    # remain, or the chosen feature is constant (min == max, no way to split).
    # Otherwise: rng.integers(0, n_features) for the feature,
    # rng.uniform(min, max) for the threshold, split on
    # column < threshold, recurse on each side with max_depth - 1.
    pass


def path_length(tree: dict, x: np.ndarray, current_depth: int = 0) -> float:
    """
    Returns:
        the number of splits needed to isolate x, plus a correction
        term for the leaf's remaining, un-split sample count:
        2*(ln(n-1) + 0.5772156649) - 2*(n-1)/n for a leaf with n
        samples (0 if n <= 1), the average path length an unsuccessful
        binary search tree lookup would take over n items.
    """
    # TODO: If tree is a leaf, return current_depth + that correction
    # term. Otherwise, recurse left or right based on
    # x[tree["feature"]] < tree["threshold"], incrementing current_depth.
    pass


def isolation_forest_fit(
    input: np.ndarray, n_trees: int, max_depth: int, seed: int | None = None
) -> list[dict]:
    """Builds n_trees independent isolation trees, each on the FULL input (no bootstrapping)."""
    # TODO: One rng, built once. Build n_trees trees with it.
    pass


def anomaly_scores(forest: list[dict], input: np.ndarray, sample_size: int) -> np.ndarray:
    """
    Returns:
        shape (n_samples,): anomaly score in (0, 1] for every row of
        input, 2^(-average_path_length / c(sample_size)), c(sample_size)
        being the same correction term path_length uses, evaluated at
        sample_size. Higher score means more anomalous (shorter average
        path to isolate).
    """
    # TODO: For each row of input, average its path_length() across
    # every tree in the forest, then plug into the formula above.
    pass
