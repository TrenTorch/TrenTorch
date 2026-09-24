"""
pytest data/app_data/01-numpy/07-linear-algebra/06-solving-linear-systems/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
solve_system = _module.solve_system
solve_via_inverse = _module.solve_via_inverse
solutions_agree = _module.solutions_agree


def test_solve_system_correctness():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    x = solve_system(A, b)
    np.testing.assert_allclose(A @ x, b)
    np.testing.assert_allclose(x, [2.0, 1.0])


def test_solve_via_inverse_produces_same_solution_as_solve_system():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    np.testing.assert_allclose(solve_system(A, b), solve_via_inverse(A, b))


def test_solutions_agree_correctly_reports_agreement():
    A = np.array([[3.0, 2.0], [1.0, 4.0]])
    b = np.array([7.0, 9.0])
    assert solutions_agree(A, b) is True


def test_solving_raises_error_for_singular_coefficient_matrix():
    singular = np.array([[1.0, 2.0], [2.0, 4.0]])
    b = np.array([1.0, 2.0])
    try:
        x = solve_system(singular, b)
    except np.linalg.LinAlgError:
        return
    # Some numpy/LAPACK backends (e.g. in-browser Pyodide builds) may not
    # raise for an exactly-singular matrix; in that case the "solution"
    # must not actually satisfy the system, or must be non-finite.
    residual = singular @ x - b
    assert not np.all(np.isfinite(x)) or np.linalg.norm(residual) > 1e-6


def test_larger_system_3_unknowns():
    A = np.array([[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]])
    b = np.array([8.0, -11.0, -3.0])
    x = solve_system(A, b)
    np.testing.assert_allclose(A @ x, b, atol=1e-8)
