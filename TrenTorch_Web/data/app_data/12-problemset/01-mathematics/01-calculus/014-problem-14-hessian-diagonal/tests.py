"""Tests compare against the exact second derivatives (the Hessian diagonal) of closed-form functions."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve

TOL = dict(rtol=1e-4, atol=1e-4)


def test_01_sum_of_squares():
    got = solve(lambda z: float(np.sum(z ** 2)), [1.0, 2.0], h=1e-3)
    np.testing.assert_allclose(got, [2.0, 2.0], **TOL)


def test_02_sum_of_cubes():
    got = solve(lambda z: float(np.sum(z ** 3)), [1.0, 2.0], h=1e-3)
    np.testing.assert_allclose(got, [6.0, 12.0], **TOL)


def test_03_linear_function_has_zero_curvature():
    got = solve(lambda z: float(3 * z[0] - 2 * z[1]), [0.5, -1.5], h=1e-3)
    np.testing.assert_allclose(got, [0.0, 0.0], atol=1e-4)


def test_04_cross_term_does_not_affect_diagonal():
    got = solve(lambda z: float(z[0] * z[1]), [2.0, 3.0], h=1e-3)
    np.testing.assert_allclose(got, [0.0, 0.0], atol=1e-4)


def test_05_exponential_sum():
    z = np.array([0.0, 1.0, -1.0])
    got = solve(lambda v: float(np.sum(np.exp(v))), z, h=1e-3)
    np.testing.assert_allclose(got, np.exp(z), **TOL)


def test_06_mixed_polynomial():
    # f = z0^2 * z1^3  ->  d2/dz0^2 = 2*z1^3,  d2/dz1^2 = 6*z0^2*z1
    got = solve(lambda z: float(z[0] ** 2 * z[1] ** 3), [2.0, 1.5], h=1e-3)
    np.testing.assert_allclose(got, [2 * 1.5 ** 3, 6 * 4.0 * 1.5], **TOL)


def test_07_quartic_at_negative_point():
    got = solve(lambda z: float(np.sum(z ** 4)), [-1.0, 0.5], h=1e-3)
    np.testing.assert_allclose(got, [12 * 1.0, 12 * 0.25], **TOL)


def test_08_single_variable():
    got = solve(lambda z: float(np.sin(z[0])), [np.pi / 2], h=1e-3)
    np.testing.assert_allclose(got, [-1.0], **TOL)


def test_09_scaling_the_function_scales_the_curvature():
    f = lambda z: float(np.sum(z ** 2))
    base = solve(f, [1.0, -1.0], h=1e-3)
    scaled = solve(lambda z: 5 * f(z), [1.0, -1.0], h=1e-3)
    np.testing.assert_allclose(scaled, 5 * base, **TOL)


def test_10_default_step_is_close_for_a_quadratic():
    got = solve(lambda z: float(np.sum(z ** 2)), [1.0, 2.0])
    np.testing.assert_allclose(got, [2.0, 2.0], atol=1e-3)


def test_11_output_length_matches_input():
    assert len(solve(lambda z: float(np.sum(z ** 2)), [1.0, 2.0, 3.0, 4.0], h=1e-3)) == 4
