"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/03-combinatorics/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/03-combinatorics")
permutations_count = _module.permutations_count
combinations_count = _module.combinations_count


# ---- 1-2: basic correctness ----


def test_1_permutations_of_3_items_taken_2_at_a_time():
    # AB, BA, AC, CA, BC, CB
    assert permutations_count(3, 2) == 6


def test_2_combinations_of_3_items_taken_2_at_a_time():
    # {A,B}, {A,C}, {B,C}
    assert combinations_count(3, 2) == 3


# ---- shape / general-case coverage ----


def test_3_permutations_larger_case():
    # 5P3 = 5*4*3 = 60
    assert permutations_count(5, 3) == 60


def test_4_combinations_larger_case():
    # 5C3 = 10
    assert combinations_count(5, 3) == 10


def test_5_permutations_count_is_always_at_least_combinations_count():
    for n, k in [(6, 2), (7, 4), (10, 1)]:
        assert permutations_count(n, k) >= combinations_count(n, k)


# ---- edge cases ----


def test_6_choosing_zero_items_has_exactly_one_way():
    assert permutations_count(5, 0) == 1
    assert combinations_count(5, 0) == 1


def test_7_choosing_all_n_items_as_a_combination_has_exactly_one_way():
    assert combinations_count(4, 4) == 1


def test_8_permuting_all_n_items_equals_n_factorial():
    import math

    assert permutations_count(4, 4) == math.factorial(4)


# ---- mutation-catching ----


def test_9_permutations_and_combinations_differ_when_order_matters():
    # A wrong implementation that always divides by k! (even for
    # permutations) would collapse the two functions to the same value.
    assert permutations_count(4, 2) == 12
    assert combinations_count(4, 2) == 6
    assert permutations_count(4, 2) != combinations_count(4, 2)


def test_10_combinations_is_symmetric_in_k_and_n_minus_k():
    # A wrong implementation of n!/(k!(n-k)!) that mishandles the
    # denominator would break this symmetry (C(n,k) == C(n,n-k)).
    assert combinations_count(8, 3) == combinations_count(8, 5)


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    # 7P4 = 7*6*5*4 = 840; 7C4 = 840 / 4! = 35
    assert permutations_count(7, 4) == 840
    assert combinations_count(7, 4) == 35
