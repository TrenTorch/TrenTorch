"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
describe_ndarray_basics = _module.describe_ndarray_basics


def test_correct_dtype_reporting_across_types():
    default_int_dtype = str(np.array([1, 2, 3]).dtype)
    assert describe_ndarray_basics(np.array([1, 2, 3]))["dtype"] == default_int_dtype
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
