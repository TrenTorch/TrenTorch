"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/15-trace-of-a-matrix/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/01-linear-algebra/15-trace-of-a-matrix")
trace = _module.trace
trace_of_product = _module.trace_of_product


# ---- 1-2: basic correctness ----


def test_1_trace_of_a_2x2_matrix():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert trace(A) == 5.0


def test_2_trace_of_product_matches_direct_computation():
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # (2, 3)
    B = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # (3, 2)
    expected = np.trace(A @ B)
    assert np.isclose(trace_of_product(A, B), expected)


# ---- shape / general-case coverage ----


def test_3_trace_of_identity_matrix():
    assert trace(np.eye(5)) == 5.0


def test_4_trace_of_a_3x3_matrix():
    A = np.array([[2.0, 0.0, 1.0], [0.0, 3.0, 0.0], [1.0, 0.0, 4.0]])
    assert trace(A) == 9.0


def test_5_trace_of_product_with_square_inputs():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])
    expected = np.trace(A @ B)
    assert np.isclose(trace_of_product(A, B), expected)


# ---- edge cases ----


def test_6_trace_of_a_1x1_matrix():
    assert trace(np.array([[7.0]])) == 7.0


def test_7_trace_with_negative_diagonal_entries():
    A = np.array([[-1.0, 5.0], [2.0, -3.0]])
    assert trace(A) == -4.0


def test_8_trace_of_zero_matrix():
    assert trace(np.zeros((4, 4))) == 0.0


# ---- mutation-catching ----


def test_9_trace_only_sums_diagonal_not_all_entries():
    # A wrong implementation summing everything (A.sum()) instead of just
    # the diagonal would give a different (larger) answer here.
    A = np.array([[1.0, 100.0], [100.0, 1.0]])
    assert trace(A) == 2.0


def test_10_cyclic_property_holds_for_non_square_ab():
    # tr(AB) == tr(BA) even though AB and BA can be different sizes --
    # verifies trace_of_product isn't accidentally computing something
    # else that happens to match only in the square case.
    A = np.array([[1.0, 2.0, 3.0]])  # (1, 3)
    B = np.array([[4.0], [5.0], [6.0]])  # (3, 1)
    ab_trace = trace_of_product(A, B)  # trace of (1,1) A@B
    ba_trace = trace_of_product(B, A)  # trace of (3,3) B@A
    assert np.isclose(ab_trace, ba_trace)


def test_11_trace_of_product_does_not_require_square_a_or_b():
    A = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 2.0]])  # (3, 2)
    B = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0]])  # (2, 3)
    expected = np.trace(A @ B)
    assert np.isclose(trace_of_product(A, B), expected)


# ---- independent oracle ----


def test_12_matches_a_hand_computed_reference_case():
    A = np.array([[3.0, 0.0], [0.0, 7.0]])
    assert trace(A) == 10.0
    B = np.array([[2.0, 0.0], [0.0, 2.0]])
    # A @ B = [[6, 0], [0, 14]], trace = 20
    assert np.isclose(trace_of_product(A, B), 20.0)
