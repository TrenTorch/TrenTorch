"""
pytest data/app_data/07-vision/02-pooling/04-metaconstellation-downsampling/tests.py
"""

import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
max_pool = _module.max_pool

# The judge allows 1 second. These tests allow more because the browser runs
# Python noticeably slower than a judge does; they still catch an accidental
# quadratic-in-window slowdown or per-window copying.
BIG_GRID_SECONDS = 6.0


def _reference(grid, f):
    """The obvious NumPy answer: view the grid as blocks and take each block's max."""
    array = np.array(grid, dtype=float)
    m = array.shape[0] // f
    return array.reshape(m, f, m, f).max(axis=(1, 3))


def _assert_same(result, expected):
    got = np.array(result, dtype=float)
    assert got.shape == expected.shape, f"expected shape {expected.shape}, got {got.shape}"
    assert np.array_equal(got, expected), "pooled values differ from the reference"


EXAMPLE_ONE = [
    [1.0, 2.0, 0.5, 0.1],
    [3.0, 4.0, 1.5, 1.1],
    [0.0, -1.0, 5.0, 2.0],
    [2.0, 1.0, 3.0, 4.0],
]


def test_example_one_matches_the_specs_worked_patches():
    result = max_pool(EXAMPLE_ONE, 2)
    assert [[float(v) for v in row] for row in result] == [[4.0, 1.5], [2.0, 5.0]]


def test_example_two_all_negative_grid_returns_its_real_maximum():
    grid = [
        [-3.5, -2.0, -7.25, -1.5],
        [-9.0, -4.0, -6.0, -8.0],
        [-2.5, -3.0, -1.25, -5.0],
        [-7.0, -6.5, -4.5, -2.75],
    ]
    result = max_pool(grid, 4)
    assert len(result) == 1 and len(result[0]) == 1
    assert float(result[0][0]) == -1.25


def test_negative_patches_are_not_clamped_to_zero():
    # A running maximum that starts at 0.0 would return 0.0 for every cell here.
    rng = random.Random(11)
    grid = [[-rng.uniform(0.5, 100.0) for _ in range(6)] for _ in range(6)]
    result = max_pool(grid, 3)
    expected = _reference(grid, 3)
    assert (expected < 0).all()
    _assert_same(result, expected)


def test_window_of_one_returns_an_equal_but_separate_copy():
    grid = [[float(i * 5 + j) - 10.0 for j in range(5)] for i in range(5)]
    result = max_pool(grid, 1)
    _assert_same(result, np.array(grid, dtype=float))

    # Changing the result must not change the input.
    result[0][0] = 12345.0
    assert grid[0][0] == -10.0


def test_window_the_size_of_the_grid_gives_one_value():
    rng = random.Random(5)
    grid = [[rng.uniform(-50.0, 50.0) for _ in range(8)] for _ in range(8)]
    result = max_pool(grid, 8)
    assert len(result) == 1 and len(result[0]) == 1
    assert float(result[0][0]) == max(max(row) for row in grid)


def test_output_is_n_over_f_by_n_over_f():
    for n, f in [(2, 1), (2, 2), (6, 2), (6, 3), (9, 3), (12, 4), (10, 5)]:
        grid = [[float(i + j) for j in range(n)] for i in range(n)]
        result = max_pool(grid, f)
        assert len(result) == n // f, f"n={n}, f={f}: wrong number of rows"
        assert all(len(row) == n // f for row in result), f"n={n}, f={f}: wrong row length"


def test_matches_a_numpy_reference_on_random_grids():
    rng = random.Random(20260921)
    for _ in range(40):
        f = rng.randint(1, 6)
        m = rng.randint(1, 7)
        n = f * m
        grid = [[rng.choice([-1, 1]) * rng.uniform(0, 1000) for _ in range(n)] for _ in range(n)]
        _assert_same(max_pool(grid, f), _reference(grid, f))


def test_repeated_values_and_ties_are_fine():
    grid = [[2.0] * 6 for _ in range(6)]
    result = max_pool(grid, 3)
    _assert_same(result, np.full((2, 2), 2.0))


def test_the_input_grid_is_not_modified():
    grid = [row[:] for row in EXAMPLE_ONE]
    max_pool(grid, 2)
    assert grid == EXAMPLE_ONE


def test_one_hot_pixel_in_a_large_sparse_grid_is_preserved():
    # 1000 x 1000 of zeros with a single bright pixel. Only the window that
    # contains it may be non-zero.
    n, f = 1000, 10
    grid = np.zeros((n, n)).tolist()
    grid[703][5] = 9.5

    start = time.perf_counter()
    result = max_pool(grid, f)
    elapsed = time.perf_counter() - start

    out = np.array(result, dtype=float)
    assert out.shape == (100, 100)
    assert out[70, 0] == 9.5
    out[70, 0] = 0.0
    assert not out.any(), "a cell other than the one holding the hot pixel is non-zero"
    assert elapsed < BIG_GRID_SECONDS, f"took {elapsed:.2f}s on a 1000 x 1000 grid"


def test_extreme_downsampling_of_a_large_grid():
    # N = 1000, F = 500 gives a 2 x 2 result, with large windows.
    rng = np.random.default_rng(7)
    array = rng.uniform(-1000, 1000, size=(1000, 1000))
    grid = array.tolist()

    start = time.perf_counter()
    result = max_pool(grid, 500)
    elapsed = time.perf_counter() - start

    _assert_same(result, _reference(grid, 500))
    assert elapsed < BIG_GRID_SECONDS, f"took {elapsed:.2f}s on a 1000 x 1000 grid"


def test_a_large_all_negative_grid_is_not_clamped_to_zero():
    rng = np.random.default_rng(3)
    array = -rng.uniform(1.0, 500.0, size=(600, 600))
    grid = array.tolist()
    result = max_pool(grid, 20)
    expected = _reference(grid, 20)
    assert (expected < 0).all()
    _assert_same(result, expected)
