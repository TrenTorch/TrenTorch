"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
contiguity_flags = _module.contiguity_flags
contiguity_of_ops = _module.contiguity_of_ops


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
