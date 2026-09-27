"""
pytest data/app_data/02-math-and-statistics/00-notation-and-foundations/01-summation-notation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

summation = load_solution(
    "02-math-and-statistics/00-notation-and-foundations/01-summation-notation"
).summation


# ---- 1-2: basic correctness ----


def test_1_sum_of_identity_1_to_5():
    assert summation(lambda i: i, 1, 5) == 15


def test_2_sum_of_squares_1_to_3():
    assert summation(lambda i: i * i, 1, 3) == 14


# ---- shape / general-case coverage ----


def test_3_single_term_sum():
    assert summation(lambda i: i, 4, 4) == 4


def test_4_sum_with_a_constant_summand():
    # Sum_{i=1}^{10} 5 = 5 * 10 terms = 50, not 5.
    assert summation(lambda i: 5, 1, 10) == 50


def test_5_sum_starting_above_zero():
    assert summation(lambda i: i, 3, 6) == 3 + 4 + 5 + 6


# ---- edge cases ----


def test_6_empty_sum_is_zero():
    assert summation(lambda i: i, 5, 2) == 0


def test_7_negative_range_indices():
    assert summation(lambda i: i, -2, 2) == -2 + -1 + 0 + 1 + 2


def test_8_float_valued_summand():
    result = summation(lambda i: i / 2, 1, 4)
    assert result == 0.5 + 1.0 + 1.5 + 2.0


# ---- mutation-catching ----


def test_9_hi_is_inclusive_not_exclusive():
    # A wrong implementation using range(lo, hi) (Python's usual
    # exclusive-stop convention) would give 1+2+3=6 instead of 1+2+3+4=10.
    assert summation(lambda i: i, 1, 4) == 10


def test_10_summand_is_called_per_index_not_once():
    calls = []

    def f(i):
        calls.append(i)
        return i

    summation(f, 1, 5)
    assert calls == [1, 2, 3, 4, 5]


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    # Sum_{i=1}^{6} i^2 = 1+4+9+16+25+36 = 91, computed independently.
    assert summation(lambda i: i**2, 1, 6) == 91
