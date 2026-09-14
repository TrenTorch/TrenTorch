"""
pytest data/app_data/01-classical-ml/04-ensembles/09-surge-gradient-boosted-trees/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
build_regression_tree = _module.build_regression_tree
gbdt_predict = _module.gbdt_predict


def test_example_one_single_split_two_leaves():
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([1.0, 1.0, 10.0, 10.0])
    queries = np.array([[2.0], [3.5]])
    predictions = gbdt_predict(
        X, y, T=1, lam=0.0, gamma=0.0, eta=1.0, max_depth=1, base_score=0.0, queries=queries
    )
    assert np.allclose(predictions, [1.0, 10.0], atol=1e-6)


def test_example_two_multiple_rounds_with_regularization():
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([1.0, 1.0, 10.0, 10.0])
    queries = np.array([[2.0], [3.5]])
    predictions = gbdt_predict(
        X, y, T=2, lam=1.0, gamma=0.0, eta=0.5, max_depth=1, base_score=0.0, queries=queries
    )
    assert np.allclose(predictions, [0.555556, 5.555556], atol=1e-4)


def test_single_tree_matches_example_one_structure_exactly():
    # Directly checks build_regression_tree's own split choice and leaf
    # weights against the hand-worked math in Example 1's explanation,
    # not just the end-to-end prediction.
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    g = np.array([-1.0, -1.0, -10.0, -10.0])
    h = np.ones(4)
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=0.0, max_depth=1)
    assert tree["leaf"] is False
    assert tree["feature"] == 0
    assert abs(tree["threshold"] - 2.5) < 1e-9
    assert abs(tree["left"]["weight"] - 1.0) < 1e-9
    assert abs(tree["right"]["weight"] - 10.0) < 1e-9


def test_multi_feature_tie_breaks_to_smallest_feature_index():
    # Two identical feature columns tie on gain at every candidate
    # threshold -- the winner must be feature 0, not feature 1, and the
    # exact same split/leaf values as the single-feature case.
    X = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]])
    g = np.array([-1.0, -1.0, -10.0, -10.0])
    h = np.ones(4)
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=0.0, max_depth=1)
    assert tree["leaf"] is False
    assert tree["feature"] == 0
    assert abs(tree["threshold"] - 2.5) < 1e-9


def test_gamma_pruning_forces_a_leaf_despite_positive_raw_gain():
    # The best raw split gain here is 40.5 (see Example 1's explanation) --
    # a gamma just above that must prune it back to a leaf. A common bug
    # is checking "gain > 0" and forgetting to subtract gamma first, which
    # would still split here since 40.5 > 0.
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    g = np.array([-1.0, -1.0, -10.0, -10.0])
    h = np.ones(4)
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=41.0, max_depth=1)
    assert tree == {"leaf": True, "weight": 5.5}


def test_max_depth_zero_is_always_a_single_leaf():
    # max_depth=0 must produce a leaf immediately, even though a
    # profitable split exists (gamma=0) -- an off-by-one bug here treats
    # max_depth=0 as "at least one split is still allowed."
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    g = np.array([-1.0, -1.0, -10.0, -10.0])
    h = np.ones(4)
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=0.0, max_depth=0)
    assert tree == {"leaf": True, "weight": 5.5}


def test_degenerate_constant_feature_contributes_no_candidates():
    # Feature 0 is constant across every sample here (only one distinct
    # value) -- it must contribute zero candidate thresholds, not crash
    # or divide by zero, and the split must land on feature 1 instead.
    X = np.array([[5.0, 1.0], [5.0, 2.0], [5.0, 3.0], [5.0, 4.0]])
    g = np.array([-1.0, -1.0, -10.0, -10.0])
    h = np.ones(4)
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=0.0, max_depth=1)
    assert tree["leaf"] is False
    assert tree["feature"] == 1
    assert abs(tree["threshold"] - 2.5) < 1e-9


def test_lambda_zero_leaf_is_the_plain_unregularized_mean():
    # lam=0 must degenerate to a plain (unregularized) mean of the
    # negative gradients, not a hardcoded nonzero regularizer.
    rng = np.random.default_rng(7)
    g = rng.normal(size=6)
    h = np.ones(6)
    X = rng.normal(size=(6, 3))
    tree = build_regression_tree(X, g, h, lam=0.0, gamma=0.0, max_depth=0)
    assert tree["leaf"] is True
    assert abs(tree["weight"] - (-np.mean(g))) < 1e-9


def test_many_rounds_with_small_eta_converge_far_better_than_one_round():
    # Checks gradients are recomputed fresh from the *current* ensemble
    # prediction every round, not reused/stale -- a stuck-gradient bug
    # would make T=25 barely better than T=1 instead of dramatically so.
    rng = np.random.default_rng(3)
    n = 40
    X = rng.normal(size=(n, 2))
    y = 3.0 * X[:, 0] - 2.0 * X[:, 1] + rng.normal(scale=0.1, size=n)
    base = float(np.mean(y))

    pred_1_round = gbdt_predict(
        X, y, T=1, lam=0.1, gamma=0.0, eta=0.3, max_depth=3, base_score=base, queries=X
    )
    pred_25_rounds = gbdt_predict(
        X, y, T=25, lam=0.1, gamma=0.0, eta=0.3, max_depth=3, base_score=base, queries=X
    )
    mse_1_round = float(np.mean((pred_1_round - y) ** 2))
    mse_25_rounds = float(np.mean((pred_25_rounds - y) ** 2))
    assert mse_25_rounds < mse_1_round / 100


def test_nonzero_base_score_propagates_through_every_round():
    # A partial (eta < 1, single-round) correction from a nonzero
    # base_score must actually shift the final prediction -- a bug that
    # trains as if base_score were always 0 and only adds it back at the
    # very end gives a different, wrong answer here.
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([1.0, 1.0, 10.0, 10.0])
    queries = np.array([[2.0], [3.5]])
    predictions = gbdt_predict(
        X, y, T=1, lam=1.0, gamma=0.0, eta=0.3, max_depth=1, base_score=5.0, queries=queries
    )
    assert np.allclose(predictions, [4.2, 6.0], atol=1e-6)


def test_predict_returns_one_value_per_query():
    rng = np.random.default_rng(11)
    X = rng.normal(size=(20, 3))
    y = rng.normal(size=20)
    queries = rng.normal(size=(9, 3))
    predictions = gbdt_predict(
        X, y, T=3, lam=0.5, gamma=0.0, eta=0.5, max_depth=2, base_score=0.0, queries=queries
    )
    assert predictions.shape == (9,)
