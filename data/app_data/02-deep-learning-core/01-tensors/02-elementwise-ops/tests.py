"""
pytest data/app_data/02-deep-learning-core/01-tensors/02-elementwise-ops/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}")
add, sub, mul, div, power = _module.add, _module.sub, _module.mul, _module.div, _module.power


def test_add_matches_hand_computation():
    assert np.array_equal(add(np.array([1, 2]), np.array([3, 4])), [4, 6])


def test_sub_matches_hand_computation():
    assert np.array_equal(sub(np.array([5, 5]), np.array([3, 1])), [2, 4])


def test_mul_matches_hand_computation():
    assert np.array_equal(mul(np.array([2, 3]), np.array([4, 5])), [8, 15])


def test_power_matches_hand_computation():
    assert np.array_equal(power(np.array([2, 3]), np.array([3, 2])), [8, 9])


def test_div_of_two_integer_arrays_returns_true_division_not_floor_division():
    result = div(np.array([7]), np.array([2]))
    assert np.isclose(result[0], 3.5)
    assert not np.isclose(result[0], 3.0)


def test_div_result_dtype_is_floating_even_for_integer_inputs():
    result = div(np.array([4, 6]), np.array([2, 4]))
    assert np.issubdtype(result.dtype, np.floating)


def test_ops_broadcast_a_scalar_against_an_array():
    assert np.array_equal(add(np.array([1, 2, 3]), 10), [11, 12, 13])
    assert np.array_equal(mul(np.array([1, 2, 3]), 2), [2, 4, 6])
