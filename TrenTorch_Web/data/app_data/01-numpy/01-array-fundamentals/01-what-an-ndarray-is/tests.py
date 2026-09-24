"""
pytest data/app_data/01-numpy/01-array-fundamentals/01-what-an-ndarray-is/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/01-array-fundamentals/{Path(__file__).resolve().parent.name}")
describe_ndarray_basics = _module.describe_ndarray_basics


def test_correct_dtype_reporting_across_types():
    assert describe_ndarray_basics(np.array([1, 2, 3]))["dtype"] == "int64"
    assert describe_ndarray_basics(np.array([1.0, 2.0]))["dtype"] == "float64"
    assert describe_ndarray_basics(np.array([True, False]))["dtype"] == "bool"


def test_correct_itemsize_per_dtype():
    assert describe_ndarray_basics(np.array([1, 2, 3], dtype=np.int64))["itemsize"] == 8
    assert describe_ndarray_basics(np.array([1, 2, 3], dtype=np.int32))["itemsize"] == 4
    assert describe_ndarray_basics(np.array([1.0], dtype=np.float64))["itemsize"] == 8


def test_consistent_itemsize_regardless_of_length():
    small = describe_ndarray_basics(np.zeros(3, dtype=np.float64))
    large = describe_ndarray_basics(np.zeros(10000, dtype=np.float64))
    assert small["itemsize"] == large["itemsize"]
