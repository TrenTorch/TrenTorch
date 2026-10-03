"""
pytest tests.py
"""

import math
from _load import load_solution

_module = load_solution(__file__)
is_valid_pmf = _module.is_valid_pmf
expected_value_discrete = _module.expected_value_discrete
binomial_pmf = _module.binomial_pmf
uniform_pdf = _module.uniform_pdf


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


# ---- 1-2: basic correctness ----


def test_1_fair_coin_flipped_once_probability_of_one_head():
    result = binomial_pmf(1, 0.5, 1)
    assert math.isclose(result, 0.5)


def test_2_uniform_density_inside_the_interval():
    result = uniform_pdf(1.5, 0.0, 2.0)
    assert math.isclose(result, 0.5)  # 1 / (2 - 0)


# ---- shape / general-case coverage ----


def test_3_binomial_pmf_of_three_heads_in_five_fair_flips():
    # C(5,3) * 0.5^3 * 0.5^2 = 10 * 0.125 * 0.25 = 0.3125
    result = binomial_pmf(5, 0.5, 3)
    assert math.isclose(result, 0.3125)


def test_4_binomial_pmf_sums_to_one_across_all_k():
    total = sum(binomial_pmf(6, 0.3, k) for k in range(7))
    assert math.isclose(total, 1.0, abs_tol=1e-9)


def test_5_uniform_density_is_zero_outside_the_interval():
    assert uniform_pdf(5.0, 0.0, 2.0) == 0.0
    assert uniform_pdf(-1.0, 0.0, 2.0) == 0.0


# ---- edge cases ----


def test_6_binomial_pmf_of_zero_successes():
    # P(X=0) for Binomial(4, 0.25) = (0.75)^4
    result = binomial_pmf(4, 0.25, 0)
    assert math.isclose(result, 0.75**4)


def test_7_binomial_pmf_of_all_successes():
    result = binomial_pmf(4, 0.25, 4)
    assert math.isclose(result, 0.25**4)


def test_8_uniform_density_exactly_at_the_boundary_is_included():
    result = uniform_pdf(0.0, 0.0, 4.0)
    assert math.isclose(result, 0.25)


# ---- mutation-catching ----


def test_9_binomial_pmf_uses_the_binomial_coefficient_not_just_p_to_the_k():
    # A wrong implementation forgetting C(n,k) would give p**k*(1-p)**(n-k)
    # = 0.5**5 = 0.03125 instead of the correct 0.3125 for n=5,k=3.
    result = binomial_pmf(5, 0.5, 3)
    assert not math.isclose(result, 0.5**3 * 0.5**2)
    assert math.isclose(result, 0.3125)


def test_10_uniform_pdf_scales_inversely_with_interval_width():
    # A wrong implementation returning a constant (ignoring a, b) would
    # give the same density regardless of interval width.
    narrow = uniform_pdf(0.5, 0.0, 1.0)
    wide = uniform_pdf(5.0, 0.0, 10.0)
    assert math.isclose(narrow, 1.0)
    assert math.isclose(wide, 0.1)
    assert narrow != wide


# ---- independent oracle ----


def test_pmf_pdf_matches_a_hand_computed_reference_case():
    # Binomial(10, 0.4), P(X=4) = C(10,4) * 0.4^4 * 0.6^6
    expected = 210 * (0.4**4) * (0.6**6)
    result = binomial_pmf(10, 0.4, 4)
    assert math.isclose(result, expected)
    assert math.isclose(uniform_pdf(3.0, 1.0, 5.0), 0.25)
