import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

k_fold_split = load_solution(
    "01-classical-ml/07-evaluation/01-splitting-and-resampling"
).k_fold_split
grid_search = load_solution("01-classical-ml/07-evaluation/04-grid-search").grid_search


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
    outer_splits = k_fold_split(input.shape[0], k_outer, seed=seed)
    outer_scores = []

    for outer_train_idx, outer_test_idx in outer_splits:
        outer_train_input, outer_train_labels = input[outer_train_idx], labels[outer_train_idx]
        outer_test_input, outer_test_labels = input[outer_test_idx], labels[outer_test_idx]

        def fit_and_score(params, outer_train_input=outer_train_input, outer_train_labels=outer_train_labels):
            inner_splits = k_fold_split(outer_train_input.shape[0], k_inner, seed=seed)
            inner_scores = []
            for inner_train_idx, inner_val_idx in inner_splits:
                predictions = train_and_predict_fn(
                    params,
                    outer_train_input[inner_train_idx],
                    outer_train_labels[inner_train_idx],
                    outer_train_input[inner_val_idx],
                )
                inner_scores.append(score_fn(outer_train_labels[inner_val_idx], predictions))
            return float(np.mean(inner_scores))

        best_params = grid_search(param_grid, fit_and_score)["best_params"]

        test_predictions = train_and_predict_fn(
            best_params, outer_train_input, outer_train_labels, outer_test_input
        )
        outer_scores.append(score_fn(outer_test_labels, test_predictions))

    return outer_scores
