import numpy as np


def adaboost_train(
    input: np.ndarray,
    labels: np.ndarray,
    n_rounds: int,
    max_depth: int = 1,
    seed: int | None = None,
) -> list[tuple[dict, float]]:
    """
    labels: {-1, +1} valued, AdaBoost's standard convention (not {0, 1}).

    Returns a list of (tree, alpha) pairs, one per round.
    """
    # TODO: weights start uniform, 1/n_samples each. One rng, built
    # once, before the loop. Each round:
    #   1. Resample the training set BY WEIGHT (rng.choice(..., p=weights))
    #      and build_tree() a shallow tree (max_depth) on that resample.
    #   2. Run that tree on the FULL original input, find the weighted
    #      error rate: sum of weights where the prediction is wrong.
    #   3. alpha = 0.5 * log((1 - weighted_error) / weighted_error).
    #      Clip weighted_error away from exactly 0 or 1 first (np.clip),
    #      to avoid log(0) or dividing by zero.
    #   4. Update weights: weights *= exp(-alpha * labels * predictions),
    #      then renormalize to sum to 1.
    #   5. Append (tree, alpha) to the ensemble.
    pass


def adaboost_predict(ensemble: list[tuple[dict, float]], input: np.ndarray) -> np.ndarray:
    """
    Weighted vote: sum alpha * (that round's prediction, {-1,+1}) across
    every round, then take the sign.
    """
    # TODO: Accumulate alpha * predict_tree(tree, input) across every
    # (tree, alpha) pair, then np.sign(...) the total.
    pass
