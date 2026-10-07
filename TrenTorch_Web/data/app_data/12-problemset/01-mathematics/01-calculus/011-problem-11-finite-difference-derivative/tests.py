"""Tests compare against the exact derivative of simple closed-form functions."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_square():
    assert solve(lambda t: t ** 2, 3.0) == pytest.approx(6.0, abs=1e-6)


def test_02_cube():
    assert solve(lambda t: t ** 3, 2.0) == pytest.approx(12.0, abs=1e-5)


def test_03_constant_function_has_zero_derivative():
    assert solve(lambda t: 7.0, 1.5) == pytest.approx(0.0, abs=1e-9)


def test_04_linear_function_has_constant_slope():
    assert solve(lambda t: 5.0 * t - 2.0, -4.0) == pytest.approx(5.0, abs=1e-6)


def test_05_sine_at_zero_is_one():
    assert solve(math.sin, 0.0) == pytest.approx(1.0, abs=1e-8)


def test_06_sine_at_pi_over_three():
    assert solve(math.sin, math.pi / 3) == pytest.approx(0.5, abs=1e-8)


def test_07_exponential():
    assert solve(math.exp, 1.0) == pytest.approx(math.e, rel=1e-8)


def test_08_logarithm():
    assert solve(math.log, 2.0) == pytest.approx(0.5, rel=1e-8)


def test_09_reciprocal_at_negative_point():
    assert solve(lambda t: 1.0 / t, -2.0) == pytest.approx(-0.25, abs=1e-8)


def test_10_cubic_polynomial_at_negative_point():
    f = lambda t: 2 * t ** 3 - t ** 2 + 4 * t
    assert solve(f, -1.0) == pytest.approx(6 * 1.0 + 2.0 + 4.0, abs=1e-5)


def test_11_larger_step_is_less_accurate_but_close():
    assert solve(lambda t: t ** 2, 3.0, h=1e-2) == pytest.approx(6.0, abs=1e-8)


def test_12_returns_python_float():
    assert isinstance(solve(lambda t: t ** 2, 1.0), float)
