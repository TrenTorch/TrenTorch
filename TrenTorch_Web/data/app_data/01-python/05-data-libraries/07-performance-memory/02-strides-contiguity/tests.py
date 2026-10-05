"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
compute_c_strides = _module.compute_c_strides
byte_offset = _module.byte_offset
slice_step_strides = _module.slice_step_strides
contiguity_flags = _module.contiguity_flags
contiguity_of_ops = _module.contiguity_of_ops


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


def test_fresh_arrays_are_c_contiguous_only():
    arr = np.arange(12).reshape(3, 4)
    result = contiguity_flags(arr)
    assert result == {"c_contiguous": True, "f_contiguous": False}


def test_1d_arrays_are_contiguous_in_both_senses():
    result = contiguity_flags(np.arange(6))
    assert result == {"c_contiguous": True, "f_contiguous": True}


def test_transpose_flips_the_flags():
    arr = np.arange(12).reshape(3, 4)
    result = contiguity_flags(arr.T)
    assert result == {"c_contiguous": False, "f_contiguous": True}


def test_contiguity_of_ops_expected_values():
    for shape in [(3, 3), (5, 4), (4, 7)]:
        arr = np.arange(shape[0] * shape[1]).reshape(shape)
        result = contiguity_of_ops(arr)
        assert result == {
            "row_slice": True,
            "column_slice": False,
            "step_slice": False,
            "transpose": False,
            "transpose_copy": True,
        }


def test_stepped_1d_slice_is_non_contiguous():
    result = contiguity_flags(np.arange(10)[::2])
    assert result == {"c_contiguous": False, "f_contiguous": False}


def test_input_not_mutated():
    arr = np.arange(12).reshape(3, 4)
    original = arr.copy()
    contiguity_of_ops(arr)
    np.testing.assert_array_equal(arr, original)
