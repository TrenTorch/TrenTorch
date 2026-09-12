"""
pytest data/app_data/00-math-and-statistics/05-data-preprocessing/04-feature-scaling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/05-data-preprocessing/{Path(__file__).resolve().parent.name}"
)
standardize = _module.standardize
min_max_normalize = _module.min_max_normalize


def test_standardize_result_has_zero_mean_and_unit_std():
    x = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0], [4.0, 40.0]])
    scaled, mean, std = standardize(x)
    assert np.allclose(scaled.mean(axis=0), 0.0, atol=1e-10)
    assert np.allclose(scaled.std(axis=0), 1.0, atol=1e-10)


def test_standardize_returns_the_computed_mean_and_std():
    x = np.array([[2.0], [4.0], [6.0]])
    _, mean, std = standardize(x)
    assert np.isclose(mean[0], 4.0)
    assert np.isclose(std[0], np.std([2.0, 4.0, 6.0]))


def test_standardize_reuses_supplied_mean_and_std_instead_of_recomputing():
    x_train = np.array([[1.0], [2.0], [3.0]])
    _, train_mean, train_std = standardize(x_train)

    x_test = np.array([[10.0]])
    scaled_test, mean_used, std_used = standardize(x_test, mean=train_mean, std=train_std)
    # Using train stats on a single test point should NOT produce
    # mean=0/std=1 (which recomputing fresh from x_test alone would give).
    assert not np.isclose(scaled_test[0, 0], 0.0)
    assert np.array_equal(mean_used, train_mean)
    assert np.array_equal(std_used, train_std)


def test_min_max_normalize_result_is_bounded_zero_to_one():
    x = np.array([[5.0, 100.0], [10.0, 200.0], [15.0, 300.0]])
    scaled, min_val, max_val = min_max_normalize(x)
    assert np.allclose(scaled.min(axis=0), 0.0)
    assert np.allclose(scaled.max(axis=0), 1.0)


def test_min_max_normalize_matches_hand_computation():
    x = np.array([[0.0], [5.0], [10.0]])
    scaled, min_val, max_val = min_max_normalize(x)
    assert np.allclose(scaled.flatten(), [0.0, 0.5, 1.0])


def test_min_max_normalize_reuses_supplied_min_max():
    x_train = np.array([[0.0], [10.0]])
    _, train_min, train_max = min_max_normalize(x_train)

    x_test = np.array([[20.0]])  # outside the training range
    scaled_test, min_used, max_used = min_max_normalize(x_test, min_val=train_min, max_val=train_max)
    # 20 is beyond the training max (10), so using train stats should
    # give a value > 1.0, not clamp to 1.0 (which fresh-fitting would).
    assert scaled_test[0, 0] > 1.0
    assert np.array_equal(min_used, train_min)


def test_standardize_computes_per_column_not_a_single_global_statistic():
    # Directly targets a mutant that computes one global mean/std across
    # the whole flattened array instead of per column (axis=0). Two
    # columns with very different scales must each get their OWN mean.
    x = np.array([[0.0, 1000.0], [2.0, 1002.0], [4.0, 1004.0]])
    _, mean, std = standardize(x)
    assert np.isclose(mean[0], 2.0)
    assert np.isclose(mean[1], 1002.0)
    assert not np.isclose(mean[0], mean[1])
