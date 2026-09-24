"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/03-vectorized-vs-loop-speed/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
multiply_with_loop = _module.multiply_with_loop
multiply_vectorized = _module.multiply_vectorized
time_both_approaches = _module.time_both_approaches


def test_both_approaches_produce_identical_results():
    arr = np.array([1.0, 2.0, 3.0, -4.0])
    np.testing.assert_allclose(multiply_with_loop(arr, 3), multiply_vectorized(arr, 3))


def test_vectorized_was_faster_for_large_array():
    arr = np.arange(200_000, dtype=float)
    result = time_both_approaches(arr, 2.0)
    assert result["vectorized_was_faster"] is True
    np.testing.assert_allclose(result["loop_result"], result["vectorized_result"])


def test_correctness_holds_for_small_array_too():
    arr = np.array([1.0, 2.0, 3.0])
    result = time_both_approaches(arr, 5.0)
    np.testing.assert_allclose(result["loop_result"], [5.0, 10.0, 15.0])
    np.testing.assert_allclose(result["vectorized_result"], [5.0, 10.0, 15.0])
