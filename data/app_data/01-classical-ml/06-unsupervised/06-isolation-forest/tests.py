"""
pytest data/app_data/01-classical-ml/06-unsupervised/06-isolation-forest/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
build_isolation_tree = _module.build_isolation_tree
path_length = _module.path_length
isolation_forest_fit = _module.isolation_forest_fit
anomaly_scores = _module.anomaly_scores


def test_max_depth_zero_gives_a_single_leaf():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(10, 2))
    tree = build_isolation_tree(input, max_depth=0, rng=rng)
    assert tree["leaf"] is True
    assert tree["size"] == 10


def test_single_sample_is_a_leaf():
    rng = np.random.default_rng(0)
    input = np.array([[1.0, 2.0]])
    tree = build_isolation_tree(input, max_depth=10, rng=rng)
    assert tree["leaf"] is True
    assert tree["size"] == 1


def test_constant_feature_becomes_a_leaf():
    rng = np.random.default_rng(0)
    input = np.array([[5.0], [5.0], [5.0]])  # only one feature, always the same value
    tree = build_isolation_tree(input, max_depth=10, rng=rng)
    assert tree["leaf"] is True


def test_path_length_on_a_pure_split_tree_matches_hand_computation():
    # A single-sample leaf has correction 0 (n<=1) -- path length is
    # exactly the split count.
    tree = {
        "leaf": False,
        "feature": 0,
        "threshold": 0.0,
        "left": {"leaf": True, "size": 1},
        "right": {
            "leaf": False,
            "feature": 0,
            "threshold": 5.0,
            "left": {"leaf": True, "size": 1},
            "right": {"leaf": True, "size": 1},
        },
    }
    assert path_length(tree, np.array([-1.0])) == 1.0  # left at depth 1
    assert path_length(tree, np.array([2.0])) == 2.0  # right, then left, depth 2
    assert path_length(tree, np.array([10.0])) == 2.0  # right, then right, depth 2


def test_path_length_includes_leaf_correction_for_unsplit_groups():
    tree = {"leaf": True, "size": 10}
    result = path_length(tree, np.array([0.0]))
    # c(10) = 2*(ln(9)+0.5772156649) - 2*9/10, a positive, non-integer value
    assert result > 0.0
    assert not np.isclose(result, 0.0)
    assert not float(result).is_integer()


def test_isolation_forest_fit_returns_requested_number_of_trees():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(30, 2))
    forest = isolation_forest_fit(input, n_trees=7, max_depth=5, seed=1)
    assert len(forest) == 7


def test_reproducible_with_the_same_seed():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(20, 2))
    forest_a = isolation_forest_fit(input, n_trees=5, max_depth=5, seed=42)
    forest_b = isolation_forest_fit(input, n_trees=5, max_depth=5, seed=42)
    assert forest_a == forest_b


def test_an_obvious_outlier_scores_much_higher_than_normal_points():
    # The actual point of the exercise, checked end to end: a point far
    # from a dense cluster must be far easier to isolate (shorter
    # average path -> higher anomaly score) than points inside the
    # cluster.
    rng = np.random.default_rng(2)
    normal_points = rng.normal(size=(100, 2))
    outlier = np.array([[15.0, 15.0]])
    input = np.vstack([normal_points, outlier])

    forest = isolation_forest_fit(input, n_trees=100, max_depth=10, seed=3)
    scores = anomaly_scores(forest, input, sample_size=input.shape[0])

    outlier_score = scores[-1]
    mean_normal_score = scores[:-1].mean()
    assert outlier_score > mean_normal_score + 0.2


def test_scores_are_never_negative_or_absurdly_large():
    rng = np.random.default_rng(5)
    input = rng.normal(size=(50, 3))
    forest = isolation_forest_fit(input, n_trees=20, max_depth=8, seed=6)
    scores = anomaly_scores(forest, input, sample_size=input.shape[0])
    assert np.all(scores > 0.0)
    assert np.all(scores <= 1.5)  # 2^(-x) for x>=0 never exceeds 1, small numerical slack
