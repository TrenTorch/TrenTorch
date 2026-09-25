"""
pytest data/app_data/01-numpy/09-performance-memory/01-strides/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/09-performance-memory/{Path(__file__).resolve().parent.name}")
compute_c_strides = _module.compute_c_strides
byte_offset = _module.byte_offset
slice_step_strides = _module.slice_step_strides


def test_compute_c_strides_matches_real_arrays():
    for shape in [(5,), (3, 4), (2, 3, 4)]:
        for itemsize, dtype in [(1, np.int8), (4, np.float32), (8, np.float64)]:
            expected = np.zeros(shape, dtype=dtype).strides
            assert compute_c_strides(shape, itemsize) == expected


def test_last_axis_stride_equals_itemsize():
    for shape in [(5,), (3, 4), (2, 3, 4), (6, 1, 2)]:
        assert compute_c_strides(shape, 8)[-1] == 8


def test_byte_offset_locates_right_element():
    arr = np.arange(24, dtype=np.int64).reshape(2, 3, 4)
    for index in [(0, 0, 0), (1, 2, 3), (0, 1, 2), (1, 0, 0)]:
        offset = byte_offset(index, arr.strides)
        assert arr.ravel()[offset // arr.itemsize] == arr[index]


def test_byte_offset_reproduces_worked_example():
    assert byte_offset((1, 2), (32, 8)) == 48
    assert byte_offset((0, 0), (32, 8)) == 0


def test_slice_step_strides_matches_real_slices():
    arr = np.arange(24).reshape(6, 4)
    for step in [1, 2, 3, -1, -2]:
        assert slice_step_strides(arr, step) == arr[::step].strides

    arr_1d = np.arange(10)
    for step in [1, 2, -1]:
        assert slice_step_strides(arr_1d, step) == arr_1d[::step].strides


def test_only_sliced_axis_stride_changes():
    arr = np.arange(60).reshape(3, 4, 5)
    result = slice_step_strides(arr, 2)
    assert result[1:] == arr.strides[1:]
    assert result[0] == arr.strides[0] * 2
