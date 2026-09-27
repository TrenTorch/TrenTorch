"""
pytest data/app_data/02-math-and-statistics/00-notation-and-foundations/04-set-and-function-notation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    "02-math-and-statistics/00-notation-and-foundations/04-set-and-function-notation"
)
is_subset = _module.is_subset
argmax = _module.argmax


# ---- 1-2: basic correctness ----


def test_1_true_subset():
    assert is_subset({1, 2}, {1, 2, 3}) is True


def test_2_argmax_of_a_simple_list():
    assert argmax([3, 7, 2, 5]) == 1


# ---- shape / general-case coverage ----


def test_3_not_a_subset():
    assert is_subset({1, 4}, {1, 2, 3}) is False


def test_4_a_set_is_a_subset_of_itself():
    assert is_subset({1, 2, 3}, {1, 2, 3}) is True


def test_5_argmax_single_element():
    assert argmax([42]) == 0


def test_6_argmax_maximum_at_the_end():
    assert argmax([1, 2, 3, 9]) == 3


# ---- edge cases ----


def test_7_empty_set_is_a_subset_of_anything():
    assert is_subset(set(), {1, 2}) is True


def test_8_empty_set_is_a_subset_of_the_empty_set():
    assert is_subset(set(), set()) is True


def test_9_argmax_with_negative_values():
    assert argmax([-5, -1, -10]) == 1


def test_10_argmax_tie_returns_first_index():
    assert argmax([3, 5, 5, 2]) == 1


# ---- mutation-catching ----


def test_11_subset_direction_matters():
    # is_subset(a, b) checks a subseteq b, not the reverse -- a wrong
    # implementation swapping the operands would flip this result.
    assert is_subset({1, 2, 3}, {1, 2}) is False


def test_12_argmax_does_not_return_the_max_value_itself():
    # A common confusion: returning the value 9 instead of its index 2.
    result = argmax([4, 1, 9])
    assert result == 2
    assert result != 9


def test_13_argmax_uses_strict_greater_than_for_ties():
    # Using >= instead of > would return the LAST tied index (2) instead
    # of the first (0).
    assert argmax([7, 3, 7]) == 0


# ---- independent oracle ----


def test_14_matches_a_hand_computed_reference_case():
    assert is_subset({2, 4}, {1, 2, 3, 4, 5}) is True
    assert argmax([10, 20, 20, 5, 30, 30]) == 4
