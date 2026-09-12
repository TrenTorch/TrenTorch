"""
pytest data/app_data/02-deep-learning-core/01-tensors/01-tensor-creation-dtype/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}")
make_tensor = _module.make_tensor
zeros = _module.zeros
ones = _module.ones
arange = _module.arange


def test_make_tensor_float_data_defaults_to_float32():
    result = make_tensor([1.0, 2.0, 3.0])
    assert result.dtype == np.float32


def test_make_tensor_int_data_keeps_numpy_inferred_dtype():
    result = make_tensor([1, 2, 3])
    assert np.issubdtype(result.dtype, np.integer)


def test_make_tensor_explicit_dtype_overrides_inference():
    result = make_tensor([1, 2, 3], dtype=np.float64)
    assert result.dtype == np.float64


def test_make_tensor_values_are_correct():
    result = make_tensor([1.5, 2.5])
    assert np.allclose(result, [1.5, 2.5])


def test_zeros_and_ones_default_to_float32():
    assert zeros((2, 3)).dtype == np.float32
    assert ones((2, 3)).dtype == np.float32


def test_zeros_and_ones_produce_correct_values_and_shape():
    z = zeros((2, 3))
    o = ones((2, 3))
    assert z.shape == (2, 3) and np.all(z == 0.0)
    assert o.shape == (2, 3) and np.all(o == 1.0)


def test_zeros_and_ones_respect_explicit_dtype():
    assert zeros((2,), dtype=np.int32).dtype == np.int32
    assert ones((2,), dtype=np.int32).dtype == np.int32


def test_arange_with_float_bounds_defaults_to_float32():
    result = arange(0.0, 5.0)
    assert result.dtype == np.float32
    assert np.allclose(result, [0.0, 1.0, 2.0, 3.0, 4.0])


def test_arange_with_int_bounds_keeps_integer_dtype():
    result = arange(0, 5)
    assert np.issubdtype(result.dtype, np.integer)
    assert np.array_equal(result, [0, 1, 2, 3, 4])


def test_arange_respects_step_and_explicit_dtype():
    result = arange(0, 10, 2, dtype=np.float32)
    assert result.dtype == np.float32
    assert np.allclose(result, [0.0, 2.0, 4.0, 6.0, 8.0])


def test_float64_default_is_not_silently_kept():
    # Directly targets a mutant that skips the float32 override
    # entirely (just returns np.array(data) unchanged): NumPy's own
    # default for float data is float64, which must NOT leak through.
    result = make_tensor([1.0, 2.0])
    assert result.dtype != np.float64
