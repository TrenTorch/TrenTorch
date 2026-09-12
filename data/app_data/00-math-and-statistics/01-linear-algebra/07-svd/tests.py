"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/07-svd/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}")
svd = _module.svd
reconstruct_from_svd = _module.reconstruct_from_svd
low_rank_approximation = _module.low_rank_approximation


def test_svd_handles_non_square_matrices():
    a = np.zeros((4, 2))
    u, singular_values, vt = svd(a)
    assert u.shape == (4, 2)
    assert singular_values.shape == (2,)
    assert vt.shape == (2, 2)


def test_singular_values_are_sorted_descending():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(5, 3))
    _, singular_values, _ = svd(a)
    assert np.all(np.diff(singular_values) <= 0)


def test_singular_values_are_never_negative():
    rng = np.random.default_rng(1)
    a = rng.normal(size=(4, 4))
    _, singular_values, _ = svd(a)
    assert np.all(singular_values >= 0.0)


def test_reconstruct_from_svd_recovers_the_original_matrix():
    rng = np.random.default_rng(2)
    a = rng.normal(size=(5, 3))
    u, singular_values, vt = svd(a)
    assert np.allclose(reconstruct_from_svd(u, singular_values, vt), a, atol=1e-10)


def test_full_rank_approximation_equals_exact_reconstruction():
    rng = np.random.default_rng(3)
    a = rng.normal(size=(4, 4))
    full_rank = min(a.shape)
    assert np.allclose(low_rank_approximation(a, full_rank), a, atol=1e-10)


def test_rank_1_approximation_of_a_rank_1_matrix_is_exact():
    # A rank-1 matrix built as an outer product: its SVD has exactly one
    # nonzero singular value, so k=1 should reconstruct it exactly.
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    a = np.outer(u, v)  # (3, 2), rank 1
    approx = low_rank_approximation(a, k=1)
    assert np.allclose(approx, a, atol=1e-8)


def test_lower_rank_approximation_has_higher_reconstruction_error():
    # A well-known property (Eckart-Young): reconstruction error is
    # monotonically non-increasing as k grows. Directly catches a mutant
    # that picks the SMALLEST singular values instead of the largest.
    rng = np.random.default_rng(4)
    a = rng.normal(size=(6, 6))
    error_k1 = np.linalg.norm(a - low_rank_approximation(a, k=1))
    error_k3 = np.linalg.norm(a - low_rank_approximation(a, k=3))
    error_k6 = np.linalg.norm(a - low_rank_approximation(a, k=6))
    assert error_k1 >= error_k3 >= error_k6
    assert np.isclose(error_k6, 0.0, atol=1e-8)
