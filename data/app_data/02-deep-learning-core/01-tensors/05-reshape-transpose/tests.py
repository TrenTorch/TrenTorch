"""
pytest data/app_data/02-deep-learning-core/01-tensors/05-reshape-transpose/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}")
reshape, transpose, permute = _module.reshape, _module.transpose, _module.permute


def test_reshape_basic():
    a = np.arange(12)
    result = reshape(a, (3, 4))
    assert result.shape == (3, 4)
    assert np.array_equal(result, a.reshape(3, 4))


def test_reshape_infers_negative_one():
    a = np.arange(12)
    result = reshape(a, (2, -1))
    assert result.shape == (2, 6)


def test_transpose_swaps_only_the_named_dims():
    a = np.arange(24).reshape(2, 3, 4)
    result = transpose(a, 0, 2)
    assert result.shape == (4, 3, 2)
    assert np.array_equal(result, np.swapaxes(a, 0, 2))


def test_permute_reorders_all_dims():
    a = np.arange(24).reshape(2, 3, 4)
    result = permute(a, (2, 0, 1))
    assert result.shape == (4, 2, 3)
    assert np.array_equal(result, np.transpose(a, (2, 0, 1)))


def test_transpose_and_permute_differ_on_a_3d_array():
    # Directly targets a mutant that implements transpose() as a full
    # permute (or vice versa): on a 3D array, swapping dims (0,2) and
    # permuting to (2,0,1) give DIFFERENT shapes/results in general.
    a = np.arange(24).reshape(2, 3, 4)
    transposed = transpose(a, 0, 2)
    permuted = permute(a, (2, 0, 1))
    assert transposed.shape != permuted.shape or not np.array_equal(transposed, permuted)


def test_transpose_on_4d_array_is_not_a_full_axis_reversal():
    # Directly targets a mutant that implements transpose(a, dim0, dim1)
    # as a full reversal of every axis (np.transpose(a) with no axes
    # argument): on a 3D array these two operations happen to coincide,
    # but on 4D they diverge in SHAPE, a real, distinguishing case a
    # 3D-only test suite would miss entirely.
    a = np.arange(120).reshape(2, 3, 4, 5)
    result = transpose(a, 0, 2)
    assert result.shape == (4, 3, 2, 5)
    assert result.shape != a.shape[::-1]


def test_transpose_leaves_untouched_dims_exactly_in_place():
    a = np.arange(24).reshape(2, 3, 4)
    result = transpose(a, 0, 2)
    assert result.shape[1] == a.shape[1]  # dimension 1 (size 3) untouched


def test_reshape_preserves_element_order():
    a = np.array([1, 2, 3, 4, 5, 6])
    result = reshape(a, (2, 3))
    assert np.array_equal(result, [[1, 2, 3], [4, 5, 6]])
