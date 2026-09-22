"""
pytest data/app_data/99-potd/01-daily/23-raw-embedding-lookup/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
embedding_lookup = _module.embedding_lookup


def test_example_matches_the_specs_worked_rows():
    E = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]])
    ids = np.array([2, 0, 3])
    np.testing.assert_allclose(
        embedding_lookup(E, ids), [[0.5, 0.6], [0.1, 0.2], [0.7, 0.8]], atol=1e-6
    )


def test_repeated_ids_return_the_same_row_each_time():
    E = np.array([[1.0, 2.0], [3.0, 4.0]])
    ids = np.array([1, 1, 0, 1])
    result = embedding_lookup(E, ids)
    np.testing.assert_allclose(result[0], result[1])
    np.testing.assert_allclose(result[1], result[3])
    assert not np.allclose(result[0], result[2])


def test_sequence_longer_than_vocabulary_is_valid():
    E = np.array([[1.0], [2.0]])
    ids = np.array([0, 1, 0, 1, 0, 1, 0])  # n=7 > V=2, all repeats
    result = embedding_lookup(E, ids)
    assert result.shape == (7, 1)


def test_non_square_vocab_and_dim_catch_a_transpose_bug():
    V, d = 5, 2
    E = np.arange(V * d, dtype=float).reshape(V, d)
    ids = np.array([4, 0, 2])
    result = embedding_lookup(E, ids)
    np.testing.assert_allclose(result, E[ids], atol=1e-9)
    assert result.shape == (3, d)


def test_matches_a_reference_on_random_tables():
    rng = np.random.default_rng(22)
    for _ in range(10):
        V = rng.integers(1, 500)
        d = rng.integers(1, 20)
        n = rng.integers(1, 500)
        E = rng.uniform(-5, 5, size=(V, d))
        ids = rng.integers(0, V, size=n)
        np.testing.assert_allclose(embedding_lookup(E, ids), E[ids], atol=1e-9)


def test_large_table_within_the_time_budget():
    import time

    rng = np.random.default_rng(23)
    E = rng.uniform(-1, 1, size=(100_000, 512))
    ids = rng.integers(0, 100_000, size=10_000)
    start = time.perf_counter()
    embedding_lookup(E, ids)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s at V=100000, d=512, n=10000"
