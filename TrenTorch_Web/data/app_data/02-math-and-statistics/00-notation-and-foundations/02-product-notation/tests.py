"""
pytest data/app_data/02-math-and-statistics/00-notation-and-foundations/02-product-notation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

product = load_solution(
    "02-math-and-statistics/00-notation-and-foundations/02-product-notation"
).product


# ---- 1-2: basic correctness ----


def test_1_product_of_identity_1_to_4():
    assert product(lambda i: i, 1, 4) == 24


def test_2_product_of_squares_1_to_3():
    assert product(lambda i: i * i, 1, 3) == 36


# ---- shape / general-case coverage ----


def test_3_single_term_product():
    assert product(lambda i: i, 4, 4) == 4


def test_4_product_with_a_constant_factor():
    # Prod_{i=1}^{4} 2 = 2^4 = 16, not 2.
    assert product(lambda i: 2, 1, 4) == 16


def test_5_product_starting_above_one():
    assert product(lambda i: i, 3, 5) == 3 * 4 * 5


# ---- edge cases ----


def test_6_empty_product_is_one():
    assert product(lambda i: i, 5, 2) == 1


def test_7_a_zero_factor_collapses_the_whole_product():
    assert product(lambda i: i, 0, 3) == 0


def test_8_negative_factor_flips_sign():
    assert product(lambda i: i, -2, 2) == 0  # includes 0
    assert product(lambda i: i, -3, -1) == -6


# ---- mutation-catching ----


def test_9_hi_is_inclusive_not_exclusive():
    # A wrong implementation using range(lo, hi) would give 1*2*3=6
    # instead of 1*2*3*4=24.
    assert product(lambda i: i, 1, 4) == 24


def test_10_accumulator_does_not_start_at_zero():
    # Starting the accumulator at 0 (copy-pasted from a summation
    # implementation) would multiply everything to 0 regardless of input.
    assert product(lambda i: i, 1, 3) == 6


def test_11_factor_is_computed_per_index_not_once():
    calls = []

    def f(i):
        calls.append(i)
        return i

    product(f, 1, 4)
    assert calls == [1, 2, 3, 4]


# ---- independent oracle ----


def test_12_matches_a_hand_computed_reference_case():
    # Prod_{i=2}^{5} (i + 1) = 3*4*5*6 = 360, computed independently.
    assert product(lambda i: i + 1, 2, 5) == 360
