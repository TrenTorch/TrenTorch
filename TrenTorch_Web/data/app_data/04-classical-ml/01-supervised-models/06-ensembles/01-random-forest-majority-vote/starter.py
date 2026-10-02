import numpy as np


def random_forest_predict(trees: list[dict], input: np.ndarray) -> np.ndarray:
    """
    trees: a list of already-built trees (03-best-split-minimal-tree's
    build_tree output), each trained independently.
    input: shape (n_samples, n_features)

    Returns:
        shape (n_samples,), the majority-vote class across every tree's
        prediction for each sample. Ties broken by the lower class label.
    """
    # TODO: Run predict_tree() for every tree in trees, collect the
    # predictions into shape (n_trees, n_samples), then for each sample
    # (each column) take the class with the most votes across trees.
    pass
