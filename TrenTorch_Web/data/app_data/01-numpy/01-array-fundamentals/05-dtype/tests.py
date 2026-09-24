"""
pytest data/app_data/01-numpy/01-array-fundamentals/05-dtype/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/01-array-fundamentals/{Path(__file__).resolve().parent.name}")
get_dtype_name = _module.get_dtype_name
create_with_dtype = _module.create_with_dtype
convert_dtype = _module.convert_dtype


def test_correct_dtype_inference():
    assert get_dtype_name(np.array([1, 2, 3])) == "int64"
    assert get_dtype_name(np.array([1.0, 2.0])) == "float64"


def test_explicit_dtype_overrides_inference():
    result = create_with_dtype([1, 2, 3], np.float32)
    assert get_dtype_name(result) == "float32"


def test_convert_dtype_truncates_rather_than_rounds():
    arr = np.array([1.9, 2.1, -1.9])
    result = convert_dtype(arr, np.int64)
    np.testing.assert_array_equal(result, [1, 2, -1])


def test_convert_dtype_does_not_mutate_original_array():
    arr = np.array([1.9, 2.1, -1.9])
    convert_dtype(arr, np.int64)
    assert get_dtype_name(arr) == "float64"
    np.testing.assert_array_equal(arr, [1.9, 2.1, -1.9])


def test_different_bit_width_dtypes_report_distinct_itemsize():
    arr32 = create_with_dtype([1, 2, 3], np.int32)
    arr64 = create_with_dtype([1, 2, 3], np.int64)
    assert arr32.itemsize == 4
    assert arr64.itemsize == 8
