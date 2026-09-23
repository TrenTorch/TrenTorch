"""
pytest data/app_data/99-potd/01-daily/26-pin-image-downsample-maxpool/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
max_pool_strided = _module.max_pool_strided


def _reference(matrix, k, s):
    H, W = matrix.shape
    out_h = (H - k) // s + 1
    out_w = (W - k) // s + 1
    out = np.empty((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            out[i, j] = matrix[i * s : i * s + k, j * s : j * s + k].max()
    return out


def test_example_matches_the_specs_worked_values():
    matrix = np.array(
        [
            [1, 3, 2, 4],
            [5, 6, 7, 8],
            [9, 1, 2, 3],
            [4, 5, 6, 0],
        ]
    )
    result = max_pool_strided(matrix, 2, 2)
    np.testing.assert_array_equal(result, [[6, 8], [9, 6]])


def test_trailing_partial_window_is_dropped_not_padded():
    # H=5, k=2, s=2: out_h = (5-2)//2 + 1 = 2, the last row is dropped.
    matrix = np.array(
        [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [100, 100],  # never touched by any full window
        ]
    )
    result = max_pool_strided(matrix, 2, 2)
    assert result.shape == (2, 1)
    np.testing.assert_array_equal(result, [[2], [4]])


def test_stride_larger_than_kernel_skips_pixels():
    # 6x6 grid, k=2, s=3: windows at (0,0)-(1,1) and (3,3)-(4,4), gaps between.
    matrix = np.arange(36).reshape(6, 6)
    result = max_pool_strided(matrix, 2, 3)
    expected = _reference(matrix, 2, 3)
    np.testing.assert_array_equal(result, expected)
    assert result.shape == (2, 2)


def test_kernel_size_one_is_pure_stride_downsampling():
    matrix = np.arange(25).reshape(5, 5)
    result = max_pool_strided(matrix, 1, 2)
    # picks every other pixel: rows 0,2,4 and cols 0,2,4
    expected = matrix[::2, ::2]
    np.testing.assert_array_equal(result, expected)


def test_overlapping_windows_when_stride_less_than_kernel():
    matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    result = max_pool_strided(matrix, 2, 1)
    expected = _reference(matrix, 2, 1)
    np.testing.assert_array_equal(result, expected)


def test_matches_a_reference_on_random_shapes():
    rng = np.random.default_rng(26)
    for _ in range(15):
        H = rng.integers(3, 20)
        W = rng.integers(3, 20)
        k = rng.integers(1, min(H, W) + 1)
        s = rng.integers(1, k + 1)
        matrix = rng.integers(-50, 50, size=(H, W))
        result = max_pool_strided(matrix, int(k), int(s))
        expected = _reference(matrix, int(k), int(s))
        np.testing.assert_array_equal(result, expected)
