"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/01-random-variables/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/01-random-variables")
is_valid_pmf = _module.is_valid_pmf
expected_value_discrete = _module.expected_value_discrete


# ---- 1-2: basic correctness ----


def test_1_fair_coin_is_a_valid_pmf():
    assert is_valid_pmf([0.5, 0.5]) is True


def test_2_expected_value_of_a_fair_die():
    result = expected_value_discrete([1, 2, 3, 4, 5, 6], [1 / 6] * 6)
    assert math.isclose(result, 3.5)


# ---- shape / general-case coverage ----


def test_3_pmf_that_does_not_sum_to_one_is_invalid():
    assert is_valid_pmf([0.5, 0.6]) is False


def test_4_pmf_with_a_negative_probability_is_invalid():
    assert is_valid_pmf([1.2, -0.2]) is False


def test_5_expected_value_of_a_biased_coin_with_heads_worth_10():
    # P(heads=1)=0.9, P(tails=0)=0.1 -> E[X] = 0.9*10 + 0.1*0 = 9.0
    result = expected_value_discrete([10, 0], [0.9, 0.1])
    assert math.isclose(result, 9.0)


# ---- edge cases ----


def test_6_single_outcome_with_probability_one_is_a_valid_pmf():
    assert is_valid_pmf([1.0]) is True


def test_7_expected_value_of_a_constant_random_variable_equals_the_constant():
    result = expected_value_discrete([7], [1.0])
    assert math.isclose(result, 7.0)


def test_8_pmf_sum_within_floating_point_tolerance_is_still_valid():
    result = is_valid_pmf([1 / 3, 1 / 3, 1 / 3])
    assert result is True


# ---- mutation-catching ----


def test_9_expected_value_uses_a_true_weighted_sum_not_a_plain_average():
    # A wrong implementation averaging outcomes (ignoring probabilities)
    # would return 5.5 here instead of the correct weighted value.
    result = expected_value_discrete([0, 10], [0.9, 0.1])
    assert math.isclose(result, 1.0)
    assert not math.isclose(result, 5.0)


def test_10_is_valid_pmf_checks_both_axioms_not_just_one():
    # Sums to 1 but has a negative entry -- a check that only verifies
    # the sum would wrongly accept this.
    assert is_valid_pmf([1.5, -0.5]) is False


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    outcomes = [1, 2, 3]
    probabilities = [0.2, 0.3, 0.5]
    assert is_valid_pmf(probabilities) is True
    # E[X] = 1*0.2 + 2*0.3 + 3*0.5 = 0.2 + 0.6 + 1.5 = 2.3
    assert math.isclose(expected_value_discrete(outcomes, probabilities), 2.3)
