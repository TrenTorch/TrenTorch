"""
pytest data/app_data/00-math-and-statistics/02-calculus/01-derivatives-first-principles/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
forward_difference = _module.forward_difference
central_difference = _module.central_difference


def test_forward_difference_of_square_matches_known_derivative():
    # f(x) = x^2, f'(x) = 2x, at x=3 -> 6
    assert np.isclose(forward_difference(lambda x: x**2, 3.0), 6.0, atol=1e-3)


def test_central_difference_of_square_matches_known_derivative():
    assert np.isclose(central_difference(lambda x: x**2, 3.0), 6.0, atol=1e-6)


def test_central_difference_of_sine_matches_cosine():
    # d/dx sin(x) = cos(x), at x=0 -> 1
    assert np.isclose(central_difference(np.sin, 0.0), 1.0, atol=1e-6)


def test_derivative_of_constant_function_is_zero():
    assert np.isclose(central_difference(lambda x: 5.0, 2.0), 0.0, atol=1e-6)


def test_derivative_of_linear_function_is_its_slope():
    assert np.isclose(central_difference(lambda x: 3.0 * x + 7.0, 1.0), 3.0, atol=1e-6)


def test_central_difference_is_more_accurate_than_forward_difference():
    # For a curved function (nonzero second derivative), central
    # difference's error should be smaller than forward difference's,
    # for the same eps -- directly tests the accuracy claim in Theory.
    f = lambda x: x**3
    true_derivative_at_2 = 12.0  # 3*x^2 at x=2
    eps = 1e-3
    forward_error = abs(forward_difference(f, 2.0, eps) - true_derivative_at_2)
    central_error = abs(central_difference(f, 2.0, eps) - true_derivative_at_2)
    assert central_error < forward_error


def test_central_difference_not_confused_with_forward_difference():
    # Directly targets a mutant that implements central_difference as a
    # copy of forward_difference (i.e. one-sided, not symmetric). Using
    # a large-ish eps on a curved function makes the two clearly diverge.
    f = lambda x: x**2
    eps = 0.1
    forward_result = forward_difference(f, 5.0, eps)
    central_result = central_difference(f, 5.0, eps)
    assert not np.isclose(forward_result, central_result, atol=1e-4)
    assert np.isclose(central_result, 10.0, atol=1e-6)  # central is exact for a quadratic
