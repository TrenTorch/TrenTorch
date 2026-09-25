"""
pytest data/app_data/02-math-and-statistics/02-calculus/07-taylor-series/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/02-calculus/07-taylor-series")
taylor_first_order = _module.taylor_first_order
taylor_second_order = _module.taylor_second_order


# ---- 1-2: basic correctness ----


def test_1_first_order_at_the_expansion_point_equals_f_of_a():
    result = taylor_first_order(lambda x: x**2, lambda x: 2 * x, 3.0, 3.0)
    assert math.isclose(result, 9.0)


def test_2_first_order_approximation_of_a_quadratic():
    # f(x) = x^2, a=2: f(2)=4, f'(2)=4. Approx at x=3: 4 + 4*(1) = 8.
    result = taylor_first_order(lambda x: x**2, lambda x: 2 * x, 2.0, 3.0)
    assert math.isclose(result, 8.0)


# ---- shape / general-case coverage ----


def test_3_second_order_at_the_expansion_point_equals_f_of_a():
    result = taylor_second_order(math.sin, math.cos, lambda x: -math.sin(x), 0.0, 0.0)
    assert math.isclose(result, 0.0, abs_tol=1e-10)


def test_4_second_order_exactly_reconstructs_a_quadratic_everywhere():
    # A degree-2 polynomial's 2nd-order Taylor expansion is EXACT at
    # every x, not just near a, since there's no 3rd-order term to omit.
    f = lambda x: x**2 + 3 * x + 1
    f_prime = lambda x: 2 * x + 3
    f_double_prime = lambda x: 2.0
    for a, x in [(0.0, 5.0), (2.0, -3.0), (1.0, 1.5)]:
        result = taylor_second_order(f, f_prime, f_double_prime, a, x)
        assert math.isclose(result, f(x), abs_tol=1e-10)


def test_5_second_order_is_closer_to_true_value_than_first_order():
    f = math.sin
    f_prime = math.cos
    f_double_prime = lambda x: -math.sin(x)
    # a=0 makes f''(0)=0 (sin is odd), so the 2nd-order term would
    # vanish there -- pick a point with non-zero curvature instead.
    a, x = 0.5, 1.5
    true_value = f(x)
    err1 = abs(true_value - taylor_first_order(f, f_prime, a, x))
    err2 = abs(true_value - taylor_second_order(f, f_prime, f_double_prime, a, x))
    assert err2 < err1


# ---- edge cases ----


def test_6_approximation_far_from_a_can_be_inaccurate_but_still_computed():
    f = math.sin
    f_prime = math.cos
    result = taylor_first_order(f, f_prime, 0.0, 100.0)
    assert isinstance(result, float)  # no crash, even though wildly off


def test_7_negative_expansion_point():
    f = lambda x: x**3
    f_prime = lambda x: 3 * x**2
    result = taylor_first_order(f, f_prime, -2.0, -2.0)
    assert math.isclose(result, -8.0)


# ---- mutation-catching ----


def test_8_first_order_uses_f_prime_not_f_double_prime_slope():
    # A wrong implementation accidentally using a curvature-like term for
    # the first-order case would diverge from the correct linear formula.
    f = lambda x: x**2
    f_prime = lambda x: 2 * x
    result = taylor_first_order(f, f_prime, 1.0, 4.0)
    # f(1) + f'(1)*(4-1) = 1 + 2*3 = 7
    assert math.isclose(result, 7.0)


def test_9_second_order_term_uses_the_1_over_2_factor():
    # A wrong implementation forgetting the /2 (or using /1) would give
    # a different (larger) result here.
    f = lambda x: x**2
    f_prime = lambda x: 2 * x
    f_double_prime = lambda x: 2.0
    result = taylor_second_order(f, f_prime, f_double_prime, 0.0, 3.0)
    # f(0) + f'(0)*3 + (2/2)*9 = 0 + 0 + 9 = 9, matches f(3)=9 exactly
    assert math.isclose(result, 9.0)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    # f(x) = e^x, a=0: f(0)=1, f'(0)=1, f''(0)=1.
    # 1st order at x=0.5: 1 + 1*0.5 = 1.5
    # 2nd order at x=0.5: 1.5 + 0.5*0.25 = 1.625
    f = math.exp
    f_prime = math.exp
    f_double_prime = math.exp
    result1 = taylor_first_order(f, f_prime, 0.0, 0.5)
    result2 = taylor_second_order(f, f_prime, f_double_prime, 0.0, 0.5)
    assert math.isclose(result1, 1.5)
    assert math.isclose(result2, 1.625)
