import numpy as np


def train_gradient_boosting(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    learning_rate: float,
) -> tuple[float, list[dict]]:
    """
    Returns:
        initial_prediction: a constant, mean(targets).
        trees: n_trees regression trees, each fit sequentially to the
        negative gradient of the ensemble's predictions so far.
    """
    # TODO: initial_prediction = mean(targets). predictions starts as
    # that constant repeated for every sample. Repeat n_trees times:
    #   fit_tree_to_negative_gradient() against the current predictions,
    #   then predictions += learning_rate * that tree's own predictions
    #   on `input`, then collect the tree.
    pass


def predict_gradient_boosting(
    initial_prediction: float,
    trees: list[dict],
    learning_rate: float,
    input: np.ndarray,
) -> np.ndarray:
    """
    Replays train_gradient_boosting's accumulation on new data:
    initial_prediction, plus learning_rate times each tree's prediction,
    summed across every tree in order.
    """
    # TODO: Start from initial_prediction (broadcast to every sample),
    # then for each tree in trees add learning_rate * predict_regression_tree(tree, input).
    pass
