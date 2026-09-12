"""
pytest data/app_data/01-classical-ml/07-evaluation/12-nested-cross-validation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

nested_cross_validation = load_solution(
    f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}"
).nested_cross_validation
grid_search = load_solution("01-classical-ml/07-evaluation/04-grid-search").grid_search
k_fold_split = load_solution(
    "01-classical-ml/07-evaluation/01-splitting-and-resampling"
).k_fold_split
knn_predict = load_solution("01-classical-ml/05-instance-based-probabilistic/01-knn").knn_predict


def _accuracy(labels, predictions):
    return float(np.mean(labels == predictions))


def _knn_train_and_predict(params, train_input, train_labels, test_input):
    return knn_predict(train_input, train_labels, test_input, k=params["k"])


def test_returns_k_outer_scores():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(40, 3))
    labels = rng.integers(0, 2, 40)
    scores = nested_cross_validation(
        input, labels, {"k": [1, 3, 5]}, k_outer=4, k_inner=3,
        train_and_predict_fn=_knn_train_and_predict, score_fn=_accuracy, seed=0,
    )
    assert len(scores) == 4


def test_achieves_high_accuracy_on_genuinely_learnable_data():
    rng = np.random.default_rng(1)
    input = rng.normal(size=(100, 2))
    labels = (input[:, 0] + input[:, 1] > 0).astype(int)
    scores = nested_cross_validation(
        input, labels, {"k": [1, 3, 5, 7, 9]}, k_outer=5, k_inner=4,
        train_and_predict_fn=_knn_train_and_predict, score_fn=_accuracy, seed=2,
    )
    assert np.mean(scores) > 0.85


def test_nested_cv_gives_an_honest_near_chance_score_on_pure_noise():
    # The core demonstration, averaged across several independent
    # datasets to smooth out per-run luck: with features that have NO
    # real relationship to the labels, nested CV's honest outer-fold
    # score should stay close to chance (0.5 for balanced binary
    # labels), not meaningfully inflated by the hyperparameter search.
    param_grid = {"k": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 21, 25, 29, 33]}
    nested_means = []
    for seed in range(6):
        rng = np.random.default_rng(seed)
        input = rng.normal(size=(80, 10))
        labels = rng.integers(0, 2, 80)
        scores = nested_cross_validation(
            input, labels, param_grid, k_outer=5, k_inner=4,
            train_and_predict_fn=_knn_train_and_predict, score_fn=_accuracy, seed=seed,
        )
        nested_means.append(np.mean(scores))

    assert 0.35 < np.mean(nested_means) < 0.6


def test_naive_non_nested_selection_is_more_optimistic_than_nested_cv():
    # The actual point of the exercise, contrasted directly: selecting
    # hyperparameters by CV over the WHOLE dataset and reporting that
    # same search's best score (the naive, leaky approach) should, on
    # average across several noise datasets, look more optimistic than
    # nested CV's honest estimate on the same data.
    param_grid = {"k": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 21, 25, 29, 33]}
    naive_scores = []
    nested_means = []
    for seed in range(6):
        rng = np.random.default_rng(seed)
        n = 80
        input = rng.normal(size=(n, 10))
        labels = rng.integers(0, 2, n)

        def naive_fit_and_score(params, input=input, labels=labels, seed=seed):
            splits = k_fold_split(n, 5, seed=seed)
            fold_scores = [
                _accuracy(
                    labels[val_idx],
                    _knn_train_and_predict(params, input[train_idx], labels[train_idx], input[val_idx]),
                )
                for train_idx, val_idx in splits
            ]
            return float(np.mean(fold_scores))

        naive_scores.append(grid_search(param_grid, naive_fit_and_score)["best_score"])

        outer_scores = nested_cross_validation(
            input, labels, param_grid, k_outer=5, k_inner=4,
            train_and_predict_fn=_knn_train_and_predict, score_fn=_accuracy, seed=seed,
        )
        nested_means.append(np.mean(outer_scores))

    assert np.mean(naive_scores) > np.mean(nested_means)


def test_inner_hyperparameter_selection_never_sees_the_outer_test_fold():
    # Directly targets a mutant that runs the inner k-fold split over
    # the FULL dataset instead of just the outer training fold (a real,
    # easy-to-write leakage bug): every row is given a unique id (its
    # own index, as the single feature), and every call to
    # train_and_predict_fn is recorded. For each outer fold, none of
    # that fold's held-out rows may appear in ANY call made while
    # selecting hyperparameters for that same fold, only in the one
    # final call that evaluates the chosen hyperparameters.
    n = 40
    input = np.arange(n).reshape(n, 1).astype(float)  # row i's id is i
    rng = np.random.default_rng(0)
    labels = rng.integers(0, 2, n)
    param_grid = {"k": [1, 3]}
    k_inner = 3
    k_outer = 4
    seed = 7

    calls = []

    def recording_train_and_predict(params, train_input, train_labels, test_input):
        calls.append(
            (set(train_input[:, 0].astype(int).tolist()), set(test_input[:, 0].astype(int).tolist()))
        )
        return knn_predict(train_input, train_labels, test_input, k=params["k"])

    nested_cross_validation(
        input, labels, param_grid, k_outer=k_outer, k_inner=k_inner,
        train_and_predict_fn=recording_train_and_predict, score_fn=_accuracy, seed=seed,
    )

    outer_splits = k_fold_split(n, k_outer, seed=seed)
    calls_per_outer_fold = len(param_grid["k"]) * k_inner + 1  # inner selection calls + 1 final call
    assert len(calls) == calls_per_outer_fold * k_outer

    for fold_idx, (_, outer_test_idx) in enumerate(outer_splits):
        outer_test_ids = set(outer_test_idx.tolist())
        start = fold_idx * calls_per_outer_fold
        fold_calls = calls[start : start + calls_per_outer_fold]

        for train_ids, test_ids in fold_calls[:-1]:  # every inner-selection call
            assert train_ids.isdisjoint(outer_test_ids)
            assert test_ids.isdisjoint(outer_test_ids)

        final_train_ids, final_test_ids = fold_calls[-1]  # the one evaluation call
        assert final_test_ids == outer_test_ids
