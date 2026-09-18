"""
pytest data/app_data/02-deep-learning-core/04-autograd/07-numerical-gradient-checking/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
numerical_gradient = _module.numerical_gradient
relative_error = _module.relative_error
gradient_check = _module.gradient_check

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value
backward = load_solution("02-deep-learning-core/04-autograd/06-minimal-autograd-engine").backward


def test_numerical_gradient_matches_known_derivative():
    result = numerical_gradient(lambda x: x**2, 3.0)
    assert np.isclose(result, 6.0, atol=1e-4)


def test_relative_error_is_zero_for_identical_values():
    assert relative_error(5.0, 5.0) == 0.0


def test_relative_error_matches_hand_computation():
    # |10 - 11| / max(10, 11, eps) = 1/11
    result = relative_error(10.0, 11.0)
    assert np.isclose(result, 1.0 / 11.0)


def test_relative_error_handles_both_values_near_zero():
    result = relative_error(1e-15, -1e-15)
    assert np.isfinite(result)


def test_gradient_check_passes_for_a_correct_gradient():
    f = lambda x: x**3
    x0 = 2.0
    correct_grad = 3 * x0**2  # 12.0
    assert gradient_check(f, x0, correct_grad) is True


def test_gradient_check_fails_for_a_deliberately_wrong_gradient():
    f = lambda x: x**3
    x0 = 2.0
    wrong_grad = 3 * x0**2 + 5.0  # deliberately off by 5
    assert gradient_check(f, x0, wrong_grad) is False


def test_gradient_check_end_to_end_with_the_autograd_engine():
    # A full-circle demonstration: check the autograd engine's own
    # analytical gradient against a numerical one, for a genuinely
    # multi-step expression with variable reuse.
    def f(x0):
        a = Value(x0)
        b = Value(3.0)
        c = a * a * b + a
        return c.data

    def analytical_grad_at(x0):
        a = Value(x0)
        b = Value(3.0)
        c = a * a * b + a
        backward(c)
        return a.grad

    x0 = 2.0
    analytical = analytical_grad_at(x0)
    assert gradient_check(f, x0, analytical) is True


def test_gradient_check_catches_a_deliberately_broken_autograd_gradient():
    def f(x0):
        a = Value(x0)
        b = Value(3.0)
        c = a * a * b + a
        return c.data

    def broken_analytical_grad_at(x0):
        a = Value(x0)
        b = Value(3.0)
        c = a * a * b + a
        backward(c)
        return a.grad + 100.0  # deliberately corrupted

    x0 = 2.0
    broken = broken_analytical_grad_at(x0)
    assert gradient_check(f, x0, broken) is False


def test_relative_error_uses_the_larger_magnitude_not_the_smaller():
    # Directly targets a mutant that divides by min(...) instead of
    # max(...): this would inflate the relative error dramatically for
    # a pair of gradients that actually agree closely in relative terms.
    result = relative_error(1000.0, 1001.0)
    assert result < 0.01  # a correct max-based relative error stays small here
