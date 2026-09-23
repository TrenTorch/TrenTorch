from typing import Callable

import numpy as np


def nested_cross_validation(
    input: np.ndarray,
    labels: np.ndarray,
    param_grid: dict,
    k_outer: int,
    k_inner: int,
    train_and_predict_fn: Callable[[dict, np.ndarray, np.ndarray, np.ndarray], np.ndarray],
    score_fn: Callable[[np.ndarray, np.ndarray], float],
    seed: int | None = None,
) -> list[float]:
    """
    train_and_predict_fn(params, train_input, train_labels, test_input)
    -> predictions: trains with the given hyperparameters and predicts
    on test_input.
    score_fn(labels, predictions) -> float: higher is better.

    Returns:
        a list of k_outer scores, one per outer fold, each computed on
        data that NEVER influenced which hyperparameters were chosen
        for that fold.
    """
    # TODO: k_fold_split(n_samples, k_outer, seed=seed) for the outer
    # folds. For each outer (train_idx, test_idx) pair:
    #   1. Define an inner fit_and_score(params) function that runs
    #      k_fold_split on the OUTER TRAINING data only (k_inner folds,
    #      same seed), trains/scores train_and_predict_fn on each inner
    #      split, and returns the mean inner score.
    #   2. grid_search(param_grid, that inner function) to pick
    #      best_params, using ONLY the outer training fold's data.
    #   3. Retrain with best_params on the FULL outer training fold,
    #      predict on the outer TEST fold (data untouched by step 1-2),
    #      score it with score_fn, append to the results list.
    pass
