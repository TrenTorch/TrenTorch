"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/02-pmf-and-pdf/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/02-pmf-and-pdf")
binomial_pmf = _module.binomial_pmf
uniform_pdf = _module.uniform_pdf


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


def test_11_matches_a_hand_computed_reference_case():
    # Binomial(10, 0.4), P(X=4) = C(10,4) * 0.4^4 * 0.6^6
    expected = 210 * (0.4**4) * (0.6**6)
    result = binomial_pmf(10, 0.4, 4)
    assert math.isclose(result, expected)
    assert math.isclose(uniform_pdf(3.0, 1.0, 5.0), 0.25)
