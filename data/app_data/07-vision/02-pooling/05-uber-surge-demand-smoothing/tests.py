"""
pytest data/app_data/07-vision/02-pooling/05-uber-surge-demand-smoothing/tests.py
"""

import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"07-vision/02-pooling/{Path(__file__).resolve().parent.name}")
avg_pool = _module.avg_pool

# The judge allows 1 second. These tests allow more because the browser runs
# Python noticeably slower than a judge does; they still catch an accidental
# quadratic-in-window slowdown or per-window copying.
BIG_GRID_SECONDS = 6.0
TOLERANCE = 1e-4


def _reference(grid, f):
    """The obvious NumPy answer: view the grid as blocks and take each block's mean."""
    array = np.array(grid, dtype=float)
    m = array.shape[0] // f
    return array.reshape(m, f, m, f).mean(axis=(1, 3))


def _assert_close(result, expected):
    got = np.array(result, dtype=float)
    assert got.shape == expected.shape, f"expected shape {expected.shape}, got {got.shape}"
    assert np.allclose(got, expected, atol=TOLERANCE), "pooled values differ from the reference"


EXAMPLE_ONE = [
    [10.0, 20.0, 5.0, 1.0],
    [30.0, 40.0, 1.0, 1.0],
    [0.0, 0.0, 50.0, 20.0],
    [0.0, 0.0, 10.0, 40.0],
]


def test_example_one_matches_the_specs_worked_patches():
    result = avg_pool(EXAMPLE_ONE, 2)
    _assert_close(result, np.array([[25.0, 2.0], [0.0, 30.0]]))


def test_normalized_features_average_correctly_across_zero():
    # z-scored demand: negatives and positives in the same patch, no clamping
    # or precision loss when the mean lands near zero.
    grid = [
        [-1.5, 1.5, 2.0, -2.0],
        [0.5, -0.5, -1.0, 1.0],
        [3.0, -3.0, 0.25, -0.25],
        [-4.0, 4.0, 0.75, -0.75],
    ]
    result = avg_pool(grid, 2)
    _assert_close(result, _reference(grid, 2))


def test_identity_pooling_when_f_equals_one():
    grid = [[float(i * 5 + j) - 10.0 for j in range(5)] for i in range(5)]
    result = avg_pool(grid, 1)
    _assert_close(result, np.array(grid, dtype=float))

    # Changing the result must not change the input.
    result[0][0] = 12345.0
    assert grid[0][0] == -10.0


def test_uniform_demand_shrinks_but_keeps_the_same_value():
    grid = [[15.5] * 12 for _ in range(12)]
    result = avg_pool(grid, 4)
    assert len(result) == 3 and all(len(row) == 3 for row in result)
    _assert_close(result, np.full((3, 3), 15.5))


def test_window_the_size_of_the_grid_gives_one_value():
    rng = random.Random(5)
    grid = [[rng.uniform(-50.0, 50.0) for _ in range(8)] for _ in range(8)]
    result = avg_pool(grid, 8)
    assert len(result) == 1 and len(result[0]) == 1
    expected = sum(sum(row) for row in grid) / 64
    assert abs(result[0][0] - expected) < TOLERANCE


def test_output_is_n_over_f_by_n_over_f():
    for n, f in [(2, 1), (2, 2), (6, 2), (6, 3), (9, 3), (12, 4), (10, 5)]:
        grid = [[float(i + j) for j in range(n)] for i in range(n)]
        result = avg_pool(grid, f)
        assert len(result) == n // f, f"n={n}, f={f}: wrong number of rows"
        assert all(len(row) == n // f for row in result), f"n={n}, f={f}: wrong row length"


def test_matches_a_numpy_reference_on_random_grids():
    rng = random.Random(20260922)
    for _ in range(40):
        f = rng.randint(1, 6)
        m = rng.randint(1, 7)
        n = f * m
        grid = [[rng.choice([-1, 1]) * rng.uniform(0, 1000) for _ in range(n)] for _ in range(n)]
        _assert_close(avg_pool(grid, f), _reference(grid, f))


def test_the_input_grid_is_not_modified():
    grid = [row[:] for row in EXAMPLE_ONE]
    avg_pool(grid, 2)
    assert grid == EXAMPLE_ONE


def test_massive_sparsity_keeps_precision_on_a_large_grid():
    # 1000 x 1000, 99%+ zeros, a handful of large values. Checks that
    # accumulation doesn't drift over big patches full of nothing.
    n, f = 1000, 20
    rng = np.random.default_rng(11)
    array = np.zeros((n, n))
    hot_rows = rng.integers(0, n, size=50)
    hot_cols = rng.integers(0, n, size=50)
    array[hot_rows, hot_cols] = rng.uniform(1e4, 1e6, size=50)
    grid = array.tolist()

    start = time.perf_counter()
    result = avg_pool(grid, f)
    elapsed = time.perf_counter() - start

    _assert_close(result, _reference(grid, f))
    assert elapsed < BIG_GRID_SECONDS, f"took {elapsed:.2f}s on a 1000 x 1000 grid"


def test_extreme_downsampling_of_a_large_grid():
    # N = 1000, F = 500 gives a 2 x 2 result, with large windows.
    rng = np.random.default_rng(7)
    array = rng.uniform(-1000, 1000, size=(1000, 1000))
    grid = array.tolist()

    start = time.perf_counter()
    result = avg_pool(grid, 500)
    elapsed = time.perf_counter() - start

    _assert_close(result, _reference(grid, 500))
    assert elapsed < BIG_GRID_SECONDS, f"took {elapsed:.2f}s on a 1000 x 1000 grid"


def test_a_large_all_negative_grid_averages_correctly():
    rng = np.random.default_rng(3)
    array = -rng.uniform(1.0, 500.0, size=(600, 600))
    grid = array.tolist()
    result = avg_pool(grid, 20)
    expected = _reference(grid, 20)
    assert (expected < 0).all()
    _assert_close(result, expected)
