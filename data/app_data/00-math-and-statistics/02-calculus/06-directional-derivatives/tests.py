"""
pytest data/app_data/00-math-and-statistics/02-calculus/06-directional-derivatives/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
directional_derivative = _module.directional_derivative
steepest_ascent_direction = _module.steepest_ascent_direction


def _f(x):
    return x[0] ** 2 + x[1] ** 2


def test_directional_derivative_along_x_axis_matches_partial_derivative():
    # df/dx at (1, 2) is 2*1 = 2
    result = directional_derivative(_f, np.array([1.0, 2.0]), np.array([1.0, 0.0]))
    assert np.isclose(result, 2.0, atol=1e-3)


def test_directional_derivative_along_y_axis_matches_partial_derivative():
    # df/dy at (1, 2) is 2*2 = 4
    result = directional_derivative(_f, np.array([1.0, 2.0]), np.array([0.0, 1.0]))
    assert np.isclose(result, 4.0, atol=1e-3)


def test_directional_derivative_normalizes_non_unit_direction():
    # A direction of length 5 should give the same result as its unit form.
    x = np.array([1.0, 2.0])
    result_scaled = directional_derivative(_f, x, np.array([5.0, 0.0]))
    result_unit = directional_derivative(_f, x, np.array([1.0, 0.0]))
    assert np.isclose(result_scaled, result_unit, atol=1e-3)


def test_directional_derivative_flips_sign_for_opposite_direction():
    x = np.array([1.0, 2.0])
    forward = directional_derivative(_f, x, np.array([1.0, 0.0]))
    backward = directional_derivative(_f, x, np.array([-1.0, 0.0]))
    assert np.isclose(forward, -backward, atol=1e-3)


def test_steepest_ascent_direction_is_a_unit_vector():
    result = steepest_ascent_direction(_f, np.array([3.0, 4.0]))
    assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-3)


def test_steepest_ascent_direction_points_along_the_gradient():
    # For f = x^2 + y^2, gradient at (3, 4) is (6, 8), normalized (0.6, 0.8)
    result = steepest_ascent_direction(_f, np.array([3.0, 4.0]))
    assert np.allclose(result, [0.6, 0.8], atol=1e-3)


def test_directional_derivative_is_maximized_along_steepest_ascent_direction():
    # The core claim this question exists to demonstrate: no other unit
    # direction gives a larger directional derivative than the gradient's
    # own (normalized) direction.
    x = np.array([1.0, 2.0])
    best_direction = steepest_ascent_direction(_f, x)
    best_value = directional_derivative(_f, x, best_direction)

    rng = np.random.default_rng(0)
    for _ in range(20):
        random_direction = rng.normal(size=2)
        other_value = directional_derivative(_f, x, random_direction)
        assert other_value <= best_value + 1e-3


def test_directional_derivative_along_steepest_ascent_equals_gradient_norm():
    # A precise, well-known identity: D_u f = ||gradient|| when u is the
    # normalized gradient direction itself.
    x = np.array([1.0, 2.0])
    best_direction = steepest_ascent_direction(_f, x)
    result = directional_derivative(_f, x, best_direction)
    gradient_norm = np.linalg.norm(np.array([2.0, 4.0]))  # analytical gradient at (1, 2)
    assert np.isclose(result, gradient_norm, atol=1e-3)


def test_steepest_ascent_direction_not_confused_with_raw_unnormalized_gradient():
    # Directly targets a mutant that returns the raw gradient instead of
    # normalizing it: the raw gradient at (3, 4) is (6, 8), norm 10, not 1.
    result = steepest_ascent_direction(_f, np.array([3.0, 4.0]))
    assert not np.allclose(result, [6.0, 8.0], atol=1e-2)
    assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-3)
