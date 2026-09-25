"""
pytest data/app_data/01-numpy/10-bridging-to-tensors/02-views-broadcasting-vectorization/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/10-bridging-to-tensors/{Path(__file__).resolve().parent.name}")
predict_broadcast_shape = _module.predict_broadcast_shape
classify_by_memory = _module.classify_by_memory
standardize_columns = _module.standardize_columns


def test_compatible_broadcast_shapes():
    pairs = [
        ((2, 3), (2, 3)),
        ((3, 1), (1, 4)),
        ((5,), (2, 5)),
        ((), (3, 4)),
        ((4, 1, 3), (1, 5, 3)),
    ]
    for a, b in pairs:
        assert predict_broadcast_shape(a, b) == np.broadcast_shapes(a, b)


def test_incompatible_shapes_raise():
    with pytest.raises(ValueError):
        predict_broadcast_shape((3,), (4,))
    with pytest.raises(ValueError):
        predict_broadcast_shape((2, 3), (3, 2))


def test_rule_applied_from_trailing_axis():
    assert predict_broadcast_shape((3, 1), (4,)) == (3, 4)
    assert predict_broadcast_shape((3,), (3, 1)) == (3, 3)


def test_classify_by_memory_on_standard_operations():
    arr = np.arange(12).reshape(3, 4)
    assert classify_by_memory(lambda a: a[1:3], arr) == "view"
    assert classify_by_memory(lambda a: a.T, arr) == "view"
    assert classify_by_memory(lambda a: a.reshape(4, 3), arr) == "view"
    assert classify_by_memory(lambda a: a[[0, 2]], arr) == "copy"
    assert classify_by_memory(lambda a: a[a > 5], arr) == "copy"
    assert classify_by_memory(lambda a: a + 1, arr) == "copy"
    assert classify_by_memory(lambda a: a.copy(), arr) == "copy"


def test_classify_by_memory_respects_layout():
    arr = np.arange(12).reshape(3, 4)
    assert classify_by_memory(lambda a: a.T.reshape(-1), arr) == "copy"
    assert classify_by_memory(lambda a: a.reshape(-1), arr) == "view"


def test_standardized_columns():
    arr = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    result = standardize_columns(arr)
    np.testing.assert_allclose(result.mean(axis=0), [0.0, 0.0], atol=1e-6)
    np.testing.assert_allclose(result.std(axis=0), [1.0, 1.0], atol=1e-6)
    assert result.shape == arr.shape


def test_zero_variance_column():
    arr = np.array([[5.0, 1.0], [5.0, 2.0], [5.0, 3.0]])
    result = standardize_columns(arr)
    np.testing.assert_allclose(result[:, 0], [0.0, 0.0, 0.0], atol=1e-4)
    assert not np.any(np.isnan(result))
    assert not np.any(np.isinf(result))


def test_input_not_mutated():
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    original = arr.copy()
    standardize_columns(arr)
    np.testing.assert_array_equal(arr, original)
