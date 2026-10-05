import numpy as np


def xgboost_leaf_value(gradients: np.ndarray, hessians: np.ndarray, lam: float) -> float:
    """The L2-regularized optimal constant value for a leaf: -sum(g) / (sum(h) + lam)."""
    # TODO: one line, straight from the formula above.
    pass


def xgboost_split_gain(
    gradients: np.ndarray, hessians: np.ndarray, left_mask: np.ndarray, lam: float
) -> float:
    """
    The regularized gain of a candidate split:
      0.5 * [ G_left^2/(H_left+lam) + G_right^2/(H_right+lam) - G^2/(H+lam) ]
    where G/H are the parent's total gradient/hessian sums.
    """
    # TODO: Sum gradients/hessians for the parent, the left side
    # (left_mask), and the right side (~left_mask), then plug into the
    # formula above.
    pass


def find_best_regularized_split(
    input: np.ndarray, gradients: np.ndarray, hessians: np.ndarray, lam: float
) -> tuple[int, float, float] | None:
    """Same search as find_best_regression_split, scored by xgboost_split_gain."""
    # TODO: For each feature, try every midpoint-between-consecutive-
    # unique-values threshold. Track the best (feature, threshold, gain).
    pass


def build_regularized_tree(
    input: np.ndarray,
    gradients: np.ndarray,
    hessians: np.ndarray,
    max_depth: int,
    lam: float,
) -> dict:
    """
    Same recursive structure as build_regression_tree, with two
    differences: the split criterion is xgboost_split_gain (not
    variance reduction), and a leaf's value is xgboost_leaf_value, not
    a plain mean.
    """
    # TODO: Base case (max_depth==0 or fewer than 2 samples) -> leaf
    # with xgboost_leaf_value(). Otherwise find_best_regularized_split(),
    # recurse on each side with max_depth - 1, or leaf if no split found.
    pass


def train_regularized_boosting(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    learning_rate: float,
    lam: float,
) -> tuple[float, list[dict]]:
    """
    Same accumulation loop as 04-full-boosting-loop's
    train_gradient_boosting, using build_regularized_tree instead of
    build_regression_tree. Hessians are constant (1.0 per sample) for
    squared-error loss; gradients are (prediction - target), the
    derivative of 0.5*(prediction-target)^2 with respect to prediction.
    """
    # TODO: initial_prediction = mean(targets), hessians = ones like
    # targets. Repeat n_trees times: gradients = predictions - targets,
    # build_regularized_tree() on (input, gradients, hessians, max_depth, lam),
    # predictions += learning_rate * predict_regression_tree(tree, input).
    pass


def predict_regularized_boosting(
    initial_prediction: float,
    trees: list[dict],
    learning_rate: float,
    input: np.ndarray,
) -> np.ndarray:
    """Identical replay logic to 04-full-boosting-loop's predict_gradient_boosting."""
    # TODO: initial_prediction, plus learning_rate * each tree's
    # prediction, summed across every tree.
    pass
