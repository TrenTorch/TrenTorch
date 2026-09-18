"""
pytest data/app_data/02-deep-learning-core/01-tensors/06-reduction-ops/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}")
sum_, mean_, max_ = _module.sum_, _module.mean_, _module.max_


def test_sum_over_whole_array():
    assert sum_(np.array([1.0, 2.0, 3.0])) == 6.0


def test_sum_along_an_axis():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert np.array_equal(sum_(a, axis=0), [4.0, 6.0])
    assert np.array_equal(sum_(a, axis=1), [3.0, 7.0])


def test_sum_keepdims_preserves_ndim():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = sum_(a, axis=1, keepdims=True)
    assert result.shape == (2, 1)


def test_mean_matches_hand_computation():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.isclose(mean_(a), 2.5)


def test_max_without_axis_returns_a_plain_scalar():
    a = np.array([[1.0, 9.0], [3.0, 4.0]])
    result = max_(a)
    assert np.isscalar(result) or result.shape == ()
    assert result == 9.0


def test_max_with_axis_returns_values_and_indices():
    a = np.array([[1.0, 9.0, 3.0], [7.0, 2.0, 8.0]])
    values, indices = max_(a, axis=1)
    assert np.array_equal(values, [9.0, 8.0])
    assert np.array_equal(indices, [1, 2])


def test_max_indices_are_not_dropped():
    # Directly targets a mutant that returns only np.max's values (like
    # np.max itself), silently discarding the indices torch.max
    # returns alongside them when a dim is given.
    a = np.array([[3.0, 1.0], [2.0, 9.0]])
    result = max_(a, axis=1)
    assert isinstance(result, tuple)
    assert len(result) == 2
