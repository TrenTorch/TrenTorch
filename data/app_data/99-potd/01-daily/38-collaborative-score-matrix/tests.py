"""
pytest data/app_data/99-potd/01-daily/38-collaborative-score-matrix/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
collaborative_scores = _module.collaborative_scores


def test_example_matches_the_specs_worked_values():
    U = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[2.0, 1.0], [1.0, 2.0], [0.0, 1.0]])
    result = collaborative_scores(U, V)
    np.testing.assert_allclose(result, [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0]], atol=1e-6)


def test_d_equals_one_is_an_outer_product():
    U = np.array([[2.0], [3.0], [-1.0]])
    V = np.array([[5.0], [4.0]])
    result = collaborative_scores(U, V)
    np.testing.assert_allclose(result, np.outer([2.0, 3.0, -1.0], [5.0, 4.0]), atol=1e-6)


def test_zero_row_in_u_gives_a_zero_output_row():
    U = np.array([[0.0, 0.0], [1.0, 1.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = collaborative_scores(U, V)
    assert not result[0].any()
    assert result[1].any()


def test_zero_row_in_v_gives_a_zero_output_column():
    U = np.array([[1.0, 1.0], [2.0, 2.0]])
    V = np.array([[0.0, 0.0], [1.0, 1.0]])
    result = collaborative_scores(U, V)
    assert not result[:, 0].any()
    assert result[:, 1].any()


def test_non_square_shapes_catch_a_transpose_bug():
    U = np.array([[1.0, 2.0, 3.0]])  # (1, 3)
    V = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])  # (2, 3)
    result = collaborative_scores(U, V)
    assert result.shape == (1, 2)
    np.testing.assert_allclose(result, [[1.0, 2.0]], atol=1e-6)


def test_matches_a_reference_on_random_shapes():
    rng = np.random.default_rng(34)
    for _ in range(15):
        n_users = int(rng.integers(1, 30))
        n_items = int(rng.integers(1, 30))
        d = int(rng.integers(1, 10))
        U = rng.uniform(-5, 5, size=(n_users, d))
        V = rng.uniform(-5, 5, size=(n_items, d))
        np.testing.assert_allclose(collaborative_scores(U, V), U @ V.T, atol=1e-6)


def test_max_size_within_the_time_budget():
    import time

    rng = np.random.default_rng(35)
    U = rng.uniform(-1, 1, size=(500, 128))
    V = rng.uniform(-1, 1, size=(500, 128))
    start = time.perf_counter()
    collaborative_scores(U, V)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"took {elapsed:.2f}s at 500x500, d=128"
