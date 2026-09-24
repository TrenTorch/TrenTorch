"""
pytest data/app_data/01-numpy/10-bridging-to-tensors/01-tensor-shape-dtype-device/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/10-bridging-to-tensors/{Path(__file__).resolve().parent.name}")
make_tensor_meta = _module.make_tensor_meta
cast_floats_to_tensor_default = _module.cast_floats_to_tensor_default
check_same_device = _module.check_same_device


def test_metadata_reported_correctly():
    for shape, dtype in [((5,), np.int64), ((3, 4), np.float32), ((2, 3, 4), bool)]:
        arr = np.zeros(shape, dtype=dtype)
        result = make_tensor_meta(arr, device="cuda")
        assert result["shape"] == shape
        assert result["dtype"] == str(np.dtype(dtype))
        assert result["device"] == "cuda"


def test_default_device():
    arr = np.zeros(3)
    result = make_tensor_meta(arr)
    assert result["device"] == "cpu"


def test_float64_becomes_float32():
    arr = np.array([1.5, 2.5, 3.5], dtype=np.float64)
    result = cast_floats_to_tensor_default(arr)
    assert result.dtype == np.float32
    np.testing.assert_allclose(result, arr, rtol=1e-6)
    assert result.shape == arr.shape


def test_non_float64_dtypes_are_untouched():
    for dtype in [np.int64, bool, np.float32]:
        arr = np.array([1, 0, 1], dtype=dtype)
        result = cast_floats_to_tensor_default(arr)
        assert result.dtype == arr.dtype
        np.testing.assert_array_equal(result, arr)


def test_original_not_mutated():
    arr = np.array([1.5, 2.5], dtype=np.float64)
    original_dtype = arr.dtype
    cast_floats_to_tensor_default(arr)
    assert arr.dtype == original_dtype
    np.testing.assert_array_equal(arr, [1.5, 2.5])


def test_same_device_passes_different_device_raises():
    assert check_same_device("cpu", "cpu") is None
    with pytest.raises(ValueError, match="cpu.*cuda|cuda.*cpu"):
        check_same_device("cpu", "cuda")
