"""
pytest data/app_data/00-math-and-statistics/02-calculus/05-hessian/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
hessian = _module.hessian
classify_critical_point = _module.classify_critical_point


def test_hessian_shape():
    f = lambda x: x[0] ** 2 + x[1] ** 2
    result = hessian(f, np.array([1.0, 1.0]))
    assert result.shape == (2, 2)


def test_hessian_of_quadratic_matches_known_constant_matrix():
    # f(x, y) = x^2 + 2y^2 + xy
    # Hessian: [[d2f/dx2, d2f/dxdy], [d2f/dydx, d2f/dy2]] = [[2, 1], [1, 4]]
    f = lambda x: x[0] ** 2 + 2 * x[1] ** 2 + x[0] * x[1]
    result = hessian(f, np.array([1.0, 1.0]))
    expected = np.array([[2.0, 1.0], [1.0, 4.0]])
    assert np.allclose(result, expected, atol=1e-2)


def test_hessian_of_quadratic_is_constant_everywhere():
    # A quadratic's Hessian doesn't depend on where you evaluate it.
    f = lambda x: 3 * x[0] ** 2 - x[0] * x[1] + x[1] ** 2
    h_at_origin = hessian(f, np.array([0.0, 0.0]))
    h_elsewhere = hessian(f, np.array([5.0, -3.0]))
    assert np.allclose(h_at_origin, h_elsewhere, atol=1e-2)


def test_hessian_of_linear_function_is_all_zeros():
    # A linear function has zero curvature everywhere.
    f = lambda x: 2 * x[0] + 3 * x[1] - 1
    result = hessian(f, np.array([1.0, 1.0]))
    assert np.allclose(result, np.zeros((2, 2)), atol=1e-2)


def test_hessian_is_symmetric():
    # Symmetry of mixed partials (Clairaut's theorem) for any smooth f.
    f = lambda x: x[0] ** 2 * x[1] + np.sin(x[0]) * x[1] ** 2
    result = hessian(f, np.array([1.0, 2.0]))
    assert np.allclose(result, result.T, atol=1e-2)


def test_classify_critical_point_minimum():
    assert classify_critical_point(np.array([[2.0, 0.0], [0.0, 3.0]])) == "minimum"


def test_classify_critical_point_maximum():
    assert classify_critical_point(np.array([[-2.0, 0.0], [0.0, -3.0]])) == "maximum"


def test_classify_critical_point_saddle():
    assert classify_critical_point(np.array([[1.0, 0.0], [0.0, -1.0]])) == "saddle"


def test_classify_critical_point_end_to_end_with_a_real_bowl_function():
    # f(x, y) = x^2 + y^2 has a true minimum at the origin.
    f = lambda x: x[0] ** 2 + x[1] ** 2
    h = hessian(f, np.array([0.0, 0.0]))
    assert classify_critical_point(h) == "minimum"


def test_classify_critical_point_end_to_end_with_a_real_saddle_function():
    # f(x, y) = x^2 - y^2 has a true saddle at the origin.
    f = lambda x: x[0] ** 2 - x[1] ** 2
    h = hessian(f, np.array([0.0, 0.0]))
    assert classify_critical_point(h) == "saddle"


def test_classify_critical_point_uses_a_tolerance_not_exact_zero():
    # Directly targets a mutant that checks eigenvalues > 0 exactly with
    # no tolerance: a matrix with a genuinely-zero eigenvalue (positive
    # semi-definite, not definite) should not be misreported as a clean
    # minimum by floating-point noise alone.
    nearly_zero_and_positive = np.array([[1e-9, 0.0], [0.0, 2.0]])
    result = classify_critical_point(nearly_zero_and_positive)
    assert result == "saddle"


def test_hessian_off_diagonal_is_not_confused_with_diagonal():
    # Directly targets a mutant that only fills the diagonal (pure
    # second derivatives) and leaves mixed partials at zero. This
    # function has a genuinely nonzero mixed partial (coefficient 5 on
    # the xy term contributes 5 to both H[0,1] and H[1,0]).
    f = lambda x: x[0] ** 2 + x[1] ** 2 + 5 * x[0] * x[1]
    result = hessian(f, np.array([1.0, 1.0]))
    assert not np.isclose(result[0, 1], 0.0, atol=1e-2)
    assert np.isclose(result[0, 1], 5.0, atol=1e-2)
