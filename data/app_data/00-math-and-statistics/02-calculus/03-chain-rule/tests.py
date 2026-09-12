"""
pytest data/app_data/00-math-and-statistics/02-calculus/03-chain-rule/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
compose = _module.compose
chain_rule_derivative = _module.chain_rule_derivative

# f(u) = u^2, f'(u) = 2u
# g(x) = 3x + 1, g'(x) = 3
_f = lambda u: u**2
_f_prime = lambda u: 2 * u
_g = lambda x: 3 * x + 1
_g_prime = lambda x: 3


def test_compose_applies_inner_then_outer():
    h = compose(_f, _g)
    # h(2) = f(g(2)) = f(7) = 49
    assert np.isclose(h(2.0), 49.0)


def test_compose_order_matters():
    h1 = compose(_f, _g)
    h2 = compose(_g, _f)
    # f(g(2)) = 49, g(f(2)) = g(4) = 13 -- clearly different
    assert not np.isclose(h1(2.0), h2(2.0))


def test_chain_rule_derivative_matches_hand_computation():
    # h(x) = (3x+1)^2, h'(x) = 2*(3x+1)*3 = 6*(3x+1), at x=2 -> 6*7 = 42
    assert np.isclose(chain_rule_derivative(_f_prime, _g, _g_prime, 2.0), 42.0)


def test_chain_rule_derivative_matches_finite_difference_of_composed_function():
    h = compose(_f, _g)
    eps = 1e-5
    numeric = (h(2.0 + eps) - h(2.0 - eps)) / (2 * eps)
    analytic = chain_rule_derivative(_f_prime, _g, _g_prime, 2.0)
    assert np.isclose(analytic, numeric, atol=1e-4)


def test_chain_rule_with_identity_inner_function_reduces_to_outer_derivative():
    identity = lambda x: x
    identity_prime = lambda x: 1.0
    # h(x) = f(x), h'(x) = f'(x) directly when g is the identity.
    assert np.isclose(
        chain_rule_derivative(_f_prime, identity, identity_prime, 5.0), _f_prime(5.0)
    )


def test_chain_rule_does_not_forget_the_inner_derivative_factor():
    # Directly targets a mutant that returns just f_prime(g(x)), forgetting
    # to multiply by g_prime(x). With g'(x) = 3 (not 1), forgetting it
    # would give 2*(3x+1) instead of the correct 6*(3x+1) -- a factor of 3 off.
    result = chain_rule_derivative(_f_prime, _g, _g_prime, 2.0)
    missing_factor_result = _f_prime(_g(2.0))
    assert not np.isclose(result, missing_factor_result)
    assert np.isclose(result, missing_factor_result * 3.0)
