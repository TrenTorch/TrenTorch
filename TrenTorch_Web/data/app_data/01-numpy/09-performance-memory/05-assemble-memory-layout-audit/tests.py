"""
pytest data/app_data/01-numpy/09-performance-memory/05-assemble-memory-layout-audit/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/09-performance-memory/{Path(__file__).resolve().parent.name}")
audit_array = _module.audit_array


def test_strides_and_expected_strides():
    arr = np.arange(12).reshape(3, 4)
    result = audit_array(arr, (2, 6))
    assert result["strides"] == arr.strides
    assert result["expected_c_strides"] == np.zeros(arr.shape, dtype=arr.dtype).strides

    transposed = arr.T
    result_t = audit_array(transposed, transposed.shape)
    assert result_t["strides"] == transposed.strides
    assert result_t["expected_c_strides"] == np.zeros(
        transposed.shape, dtype=transposed.dtype
    ).strides


def test_contiguity_agrees_with_strides():
    arr = np.arange(24).reshape(4, 6)
    for candidate in [arr, arr.T, arr[:, ::2], arr[::2]]:
        result = audit_array(candidate, (candidate.size,))
        expected_contiguous = result["strides"] == result["expected_c_strides"]
        assert result["c_contiguous"] == expected_contiguous


def test_reshape_copies_detected_correctly():
    arr = np.arange(12).reshape(3, 4)
    result = audit_array(arr, (2, 6))
    assert result["reshape_copies"] is False

    t = arr.T
    result_t = audit_array(t, (t.size,))
    assert result_t["reshape_copies"] is True


def test_contiguous_version_is_correct():
    arr = np.arange(12).reshape(3, 4)
    original = arr.copy()
    for candidate in [arr, arr.T]:
        result = audit_array(candidate, (candidate.size,))
        assert result["contiguous_version"].flags["C_CONTIGUOUS"]
        np.testing.assert_array_equal(result["contiguous_version"], candidate)
    np.testing.assert_array_equal(arr, original)


def test_conversion_copied_reflects_reality():
    arr = np.arange(12).reshape(3, 4)
    result = audit_array(arr, (2, 6))
    assert result["conversion_copied"] is False
    assert result["conversion_copied"] == (not result["c_contiguous"])

    t = arr.T
    result_t = audit_array(t, (t.size,))
    assert result_t["conversion_copied"] is True
    assert result_t["conversion_copied"] == (not result_t["c_contiguous"])


def test_nbytes_correct_across_dtypes():
    for dtype in [np.int32, np.float32, np.float64]:
        arr = np.arange(12, dtype=dtype).reshape(3, 4)
        result = audit_array(arr, (2, 6))
        assert result["nbytes"] == arr.size * arr.itemsize


def test_sum_matches_is_true():
    for arr in [np.arange(20).reshape(4, 5), np.arange(20.0).reshape(4, 5)]:
        result = audit_array(arr, (arr.size,))
        assert result["sum_matches"] is True


def test_speedup_is_real_on_sizeable_array():
    arr = np.arange(90000).reshape(300, 300)
    result = audit_array(arr, (arr.size,))
    assert result["speedup"] > 1
