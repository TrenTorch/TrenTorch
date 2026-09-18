"""
pytest data/app_data/00-math-and-statistics/06-exploratory-data-analysis/03-correlation-matrix/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/06-exploratory-data-analysis/{Path(__file__).resolve().parent.name}"
)
correlation_matrix = _module.correlation_matrix
most_correlated_pair = _module.most_correlated_pair


def test_correlation_matrix_diagonal_is_one():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 4))
    result = correlation_matrix(x)
    assert np.allclose(np.diag(result), 1.0)


def test_correlation_matrix_is_symmetric():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(50, 4))
    result = correlation_matrix(x)
    assert np.allclose(result, result.T)


def test_correlation_matrix_shape_matches_feature_count():
    x = np.zeros((10, 5))
    x[:, 0] = np.arange(10)  # avoid a zero-variance column crashing correlation
    result = correlation_matrix(x + np.random.default_rng(0).normal(scale=0.01, size=(10, 5)))
    assert result.shape == (5, 5)


def test_correlation_matrix_entries_are_bounded():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(100, 3))
    result = correlation_matrix(x)
    assert np.all(result >= -1.0 - 1e-9) and np.all(result <= 1.0 + 1e-9)


def test_correlation_matrix_matches_numpy_corrcoef():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(60, 4))
    result = correlation_matrix(x)
    expected = np.corrcoef(x.T)
    assert np.allclose(result, expected, atol=1e-9)


def test_correlation_matrix_detects_strongly_related_features():
    rng = np.random.default_rng(4)
    a = rng.normal(size=200)
    b = 3.0 * a + rng.normal(scale=0.01, size=200)  # near-perfect linear relation
    c = rng.normal(size=200)  # unrelated
    x = np.column_stack([a, b, c])
    result = correlation_matrix(x)
    assert result[0, 1] > 0.99
    assert abs(result[0, 2]) < 0.3


def test_most_correlated_pair_finds_the_strongest_relationship():
    rng = np.random.default_rng(5)
    a = rng.normal(size=200)
    b = 2.0 * a + rng.normal(scale=0.01, size=200)
    c = rng.normal(size=200)
    x = np.column_stack([a, b, c])
    corr = correlation_matrix(x)
    pair = most_correlated_pair(corr)
    assert set(pair) == {0, 1}


def test_most_correlated_pair_considers_strong_negative_correlation_too():
    corr = np.array(
        [
            [1.0, 0.1, -0.95],
            [0.1, 1.0, 0.05],
            [-0.95, 0.05, 1.0],
        ]
    )
    pair = most_correlated_pair(corr)
    assert set(pair) == {0, 2}


def test_most_correlated_pair_excludes_the_diagonal():
    # Directly targets a mutant that doesn't zero out the diagonal before
    # searching: the diagonal's trivial 1.0s would otherwise always win,
    # regardless of what the real off-diagonal relationships look like.
    corr = np.array(
        [
            [1.0, 0.2],
            [0.2, 1.0],
        ]
    )
    pair = most_correlated_pair(corr)
    assert pair[0] != pair[1]
