"""
pytest data/app_data/02-math-and-statistics/00-notation-and-foundations/05-big-o-notation/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/00-notation-and-foundations/05-big-o-notation")
count_comparisons_linear_search = _module.count_comparisons_linear_search
count_comparisons_binary_search = _module.count_comparisons_binary_search


# ---- 1-2: basic correctness ----


def test_1_linear_search_finds_target():
    found, comparisons = count_comparisons_linear_search([5, 3, 8, 1], 8)
    assert found is True
    assert comparisons == 3


def test_2_binary_search_finds_target():
    found, comparisons = count_comparisons_binary_search([1, 3, 5, 7, 9], 7)
    assert found is True


# ---- shape / general-case coverage ----


def test_3_linear_search_not_found_scans_everything():
    found, comparisons = count_comparisons_linear_search([1, 2, 3], 99)
    assert found is False
    assert comparisons == 3


def test_4_binary_search_not_found():
    found, _ = count_comparisons_binary_search([1, 2, 3, 4, 5], 6)
    assert found is False


def test_5_linear_search_stops_at_first_match():
    found, comparisons = count_comparisons_linear_search([1, 1, 1, 1], 1)
    assert found is True
    assert comparisons == 1


# ---- edge cases ----


def test_6_empty_array_linear_search():
    found, comparisons = count_comparisons_linear_search([], 5)
    assert found is False
    assert comparisons == 0


def test_7_empty_array_binary_search():
    found, comparisons = count_comparisons_binary_search([], 5)
    assert found is False
    assert comparisons == 0


def test_8_single_element_found():
    assert count_comparisons_binary_search([42], 42) == (True, 1)


def test_9_target_at_the_boundaries():
    arr = list(range(1, 11))
    found_first, _ = count_comparisons_binary_search(arr, 1)
    found_last, _ = count_comparisons_binary_search(arr, 10)
    assert found_first is True
    assert found_last is True


# ---- mutation-catching ----


def test_10_binary_search_comparison_count_grows_logarithmically():
    # A "binary search" that's secretly a linear scan would need ~1000
    # comparisons for a miss in a 1000-element array; real binary search
    # needs at most ceil(log2(1000)) + 1 ~= 11.
    arr = list(range(0, 2000, 2))  # 1000 sorted even numbers
    _, comparisons = count_comparisons_binary_search(arr, -1)  # guaranteed miss
    assert comparisons <= math.ceil(math.log2(len(arr))) + 1


def test_11_linear_search_comparison_count_matches_worst_case_n():
    arr = list(range(500))
    _, comparisons = count_comparisons_linear_search(arr, -1)  # guaranteed miss
    assert comparisons == 500


def test_12_binary_search_actually_halves_not_just_returns_correct_answer():
    # Checks the comparison count for a KNOWN miss against the exact
    # expected trace, catching an implementation that gets the right
    # found/not-found answer via some other (non-halving) method.
    arr = [1, 3, 5, 7, 9, 11, 13, 15]  # len 8
    found, comparisons = count_comparisons_binary_search(arr, 4)
    assert found is False
    assert comparisons == 3  # mid=7(idx3)->too big, mid=3(idx1)->too small, mid=5(idx2)->too big


# ---- independent oracle ----


def test_13_matches_a_hand_traced_reference_case():
    # arr = [2, 4, 6, 8, 10, 12, 14], target = 10
    # mid indices (0-based, len=7): first mid=3 -> value 8 (too small),
    # search [4..6] -> mid=5 -> value 12 (too big),
    # search [4..4] -> mid=4 -> value 10 (match). 3 comparisons.
    arr = [2, 4, 6, 8, 10, 12, 14]
    found, comparisons = count_comparisons_binary_search(arr, 10)
    assert found is True
    assert comparisons == 3
