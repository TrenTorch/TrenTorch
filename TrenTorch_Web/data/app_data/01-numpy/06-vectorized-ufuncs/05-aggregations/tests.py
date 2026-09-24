"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/05-aggregations/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
compute_summary = _module.compute_summary
sum_with_loop = _module.sum_with_loop


def test_compute_summary_correctness_for_all_seven_keys():
    arr = np.array([4, 8, 15, 16, 23, 42])
    result = compute_summary(arr)
    assert result["sum"] == 108
    assert result["mean"] == 18.0
    assert result["min"] == 4
    assert result["max"] == 42
    assert result["argmin"] == 0
    assert result["argmax"] == 5
    np.testing.assert_allclose(result["std"], arr.std())


def test_argmin_argmax_correctness_with_duplicate_extreme_values():
    arr = np.array([5, 1, 3, 1, 5])
    result = compute_summary(arr)
    assert result["argmin"] == 1
    assert result["argmax"] == 0


def test_sum_with_loop_matches_arr_sum():
    arr = np.array([-3, 5, 2, -8, 10])
    assert sum_with_loop(arr) == arr.sum()

    float_arr = np.array([1.5, 2.5, -3.25])
    np.testing.assert_allclose(sum_with_loop(float_arr), float_arr.sum())


def test_single_element_array_edge_case():
    arr = np.array([7])
    result = compute_summary(arr)
    assert result["sum"] == 7
    assert result["mean"] == 7
    assert result["min"] == 7
    assert result["max"] == 7
    assert result["argmin"] == 0
    assert result["argmax"] == 0
