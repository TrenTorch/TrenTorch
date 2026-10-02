"""
pytest tests.py
"""

import math

from _load import load_solution

_module = load_solution(__file__)
telescoping_partial_sum = _module.telescoping_partial_sum
telescoping_infinite_sum = _module.telescoping_infinite_sum
sum_reciprocal_products = _module.sum_reciprocal_products


# ---- 1-5: partial sums ----


def test_1_partial_sum_matches_a_hand_computed_case():
    # f(k) = 1/k: (1 - 1/2) + (1/2 - 1/3) + (1/3 - 1/4) = 3/4
    assert math.isclose(telescoping_partial_sum(lambda k: 1.0 / k, 3), 0.75)


def test_2_partial_sum_matches_brute_force():
    f = lambda k: k**2 / (k**2 + 1.0)
    for n in (1, 2, 7, 50):
        brute = sum(f(k) - f(k + 1) for k in range(1, n + 1))
        assert math.isclose(telescoping_partial_sum(f, n), brute, abs_tol=1e-9)


def test_3_calls_f_exactly_twice():
    calls = []

    def f(k):
        calls.append(k)
        return 1.0 / k

    telescoping_partial_sum(f, 10**6)
    assert sorted(calls) == [1, 10**6 + 1]


def test_4_zero_terms_sum_to_zero_without_calling_f():
    def f(k):
        raise AssertionError("f must not be called for an empty sum")

    assert telescoping_partial_sum(f, 0) == 0.0


def test_5_a_constant_f_gives_zero():
    assert telescoping_partial_sum(lambda k: 5.0, 100) == 0.0


# ---- 6-8: infinite sums ----


def test_6_infinite_sum_is_first_minus_limit():
    # f(k) = 1/k goes from 1 down to 0
    assert math.isclose(telescoping_infinite_sum(1.0, 0.0), 1.0)


def test_7_infinite_sum_with_a_nonzero_limit():
    # f(k) = 3 + 1/k: sum is (3 + 1) - 3 = 1
    assert math.isclose(telescoping_infinite_sum(4.0, 3.0), 1.0)


def test_8_partial_sums_approach_the_infinite_sum():
    f = lambda k: 2.0 + 1.0 / k**2
    assert math.isclose(telescoping_partial_sum(f, 10**6), telescoping_infinite_sum(3.0, 2.0), rel_tol=1e-5)


# ---- 9-12: the reciprocal-products series ----


def test_9_reciprocal_products_hand_computed():
    # 1/2 + 1/6 + 1/12 = 3/4
    assert math.isclose(sum_reciprocal_products(3), 0.75)


def test_10_reciprocal_products_match_brute_force():
    for n in (1, 2, 10, 500):
        brute = sum(1.0 / (k * (k + 1)) for k in range(1, n + 1))
        assert math.isclose(sum_reciprocal_products(n), brute, rel_tol=1e-12)


def test_11_reciprocal_products_zero_terms():
    assert sum_reciprocal_products(0) == 0.0


def test_12_reciprocal_products_approach_one():
    assert 0.999999 < sum_reciprocal_products(10**7) < 1.0
