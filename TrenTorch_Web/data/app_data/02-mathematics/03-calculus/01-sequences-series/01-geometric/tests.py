"""
pytest tests.py
"""

import math

import pytest

from _load import load_solution

_module = load_solution(__file__)
geometric_partial_sum = _module.geometric_partial_sum
geometric_series_sum = _module.geometric_series_sum
terms_needed = _module.terms_needed


def _brute_force(a, r, n):
    return sum(a * r**k for k in range(n))


# ---- 1-4: partial sums ----


def test_1_partial_sum_matches_a_hand_computed_case():
    # 1 + 2 + 4 + 8 = 15
    assert math.isclose(geometric_partial_sum(1.0, 2.0, 4), 15.0)


def test_2_partial_sum_matches_brute_force_for_many_ratios():
    for a in (1.0, -3.0, 0.5):
        for r in (-0.9, -0.5, 0.3, 0.99, 1.5, 3.0):
            for n in (1, 2, 5, 10):
                assert math.isclose(geometric_partial_sum(a, r, n), _brute_force(a, r, n), rel_tol=1e-9)


def test_3_ratio_of_one_gives_n_times_a():
    assert geometric_partial_sum(4.0, 1, 5) == 20.0
    assert geometric_partial_sum(2.5, 1.0, 3) == 7.5


def test_4_zero_terms_sum_to_zero():
    assert geometric_partial_sum(7.0, 0.5, 0) == 0.0
    assert geometric_partial_sum(7.0, 1, 0) == 0.0


def test_5_partial_sum_runs_in_constant_time_for_huge_n():
    assert math.isclose(geometric_partial_sum(1.0, 0.5, 10**9), 2.0)


# ---- 6-9: infinite sums ----


def test_6_infinite_sum_of_halves_is_two():
    assert math.isclose(geometric_series_sum(1.0, 0.5), 2.0)


def test_7_infinite_sum_with_a_negative_ratio():
    # 1 - 1/2 + 1/4 - ... = 1 / (1 + 1/2) = 2/3
    assert math.isclose(geometric_series_sum(1.0, -0.5), 2.0 / 3.0)


def test_8_partial_sums_approach_the_infinite_sum():
    assert math.isclose(geometric_partial_sum(3.0, 0.8, 200), geometric_series_sum(3.0, 0.8), rel_tol=1e-9)


@pytest.mark.parametrize("r", [1.0, -1.0, 1.5, -2.0])
def test_9_divergent_ratios_raise_value_error(r):
    with pytest.raises(ValueError):
        geometric_series_sum(1.0, r)


# ---- 10-14: how many terms ----


def test_10_terms_needed_matches_a_hand_computed_case():
    # gap after n terms is 2 * 0.5**n; below 0.01 first happens at n = 8 (2/256)
    assert terms_needed(1.0, 0.5, 0.01) == 8


def test_11_terms_needed_is_the_smallest_valid_n():
    for a, r, tol in [(1.0, 0.5, 1e-3), (5.0, 0.9, 1e-6), (-2.0, -0.7, 1e-4), (0.3, 0.1, 1e-9)]:
        n = terms_needed(a, r, tol)
        total = geometric_series_sum(a, r)
        assert abs(total - geometric_partial_sum(a, r, n)) < tol
        if n > 0:
            assert abs(total - geometric_partial_sum(a, r, n - 1)) >= tol


def test_12_already_within_tolerance_needs_zero_terms():
    assert terms_needed(1.0, 0.5, 100.0) == 0
    assert terms_needed(0.0, 0.5, 1e-9) == 0


def test_13_ratio_zero_needs_at_most_one_term():
    assert terms_needed(1.0, 0.0, 0.5) == 1


def test_14_slower_ratios_need_more_terms():
    assert terms_needed(1.0, 0.99, 1e-6) > terms_needed(1.0, 0.5, 1e-6)


@pytest.mark.parametrize("a, r, tol", [(1.0, 1.0, 0.1), (1.0, -1.5, 0.1), (1.0, 0.5, 0.0), (1.0, 0.5, -1.0)])
def test_15_invalid_arguments_raise_value_error(a, r, tol):
    with pytest.raises(ValueError):
        terms_needed(a, r, tol)
