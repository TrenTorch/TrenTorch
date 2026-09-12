"""
pytest data/app_data/00-math-and-statistics/02-calculus/02-partial-derivatives/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
partial_derivative = _module.partial_derivative
gradient = _module.gradient


def _f(x):
    # f(x, y) = x^2 + y^3
    return x[0] ** 2 + x[1] ** 3


def test_partial_derivative_wrt_first_coordinate():
    # df/dx = 2x, at (2, 3) -> 4
    assert np.isclose(partial_derivative(_f, np.array([2.0, 3.0]), 0), 4.0, atol=1e-3)


def test_partial_derivative_wrt_second_coordinate():
    # df/dy = 3y^2, at (2, 3) -> 27
    assert np.isclose(partial_derivative(_f, np.array([2.0, 3.0]), 1), 27.0, atol=1e-3)


def test_partial_derivative_does_not_mutate_input():
    x = np.array([2.0, 3.0])
    x_copy = x.copy()
    partial_derivative(_f, x, 0)
    assert np.array_equal(x, x_copy)


def test_gradient_matches_known_analytical_gradient():
    x = np.array([2.0, 3.0])
    result = gradient(_f, x)
    assert result.shape == (2,)
    assert np.allclose(result, [4.0, 27.0], atol=1e-3)


def test_gradient_of_constant_function_is_all_zeros():
    result = gradient(lambda x: 5.0, np.array([1.0, 2.0, 3.0]))
    assert np.allclose(result, [0.0, 0.0, 0.0], atol=1e-6)


def test_gradient_of_dot_product_with_fixed_vector():
    # f(x) = a . x is linear, so its gradient is just a itself, everywhere.
    a = np.array([2.0, -1.0, 3.0])
    result = gradient(lambda x: np.dot(a, x), np.array([10.0, -5.0, 0.5]))
    assert np.allclose(result, a, atol=1e-3)


def test_gradient_only_uses_the_correct_coordinate_per_entry():
    # Directly targets a mutant that always perturbs coordinate 0
    # regardless of `index` (a classic off-by-loop-variable bug): for a
    # function whose partials genuinely differ across coordinates, every
    # entry of the gradient must reflect ITS OWN coordinate's partial.
    def f(x):
        return 1.0 * x[0] + 10.0 * x[1] + 100.0 * x[2]

    result = gradient(f, np.array([1.0, 1.0, 1.0]))
    assert np.allclose(result, [1.0, 10.0, 100.0], atol=1e-3)
