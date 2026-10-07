"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [3.0, 1.0], [6.0, 2.0])
    assert numeric == pytest.approx(6.000000000039306, abs=1e-6)
    assert a0 == 6.0
    assert diff == pytest.approx(3.930633596382904e-11, abs=1e-6)


def test_exact_zero_inputs():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [0.0, 0.0], [0.0, 0.0])
    assert numeric == pytest.approx(0.0, abs=1e-6)
    assert a0 == 0.0
    assert diff == pytest.approx(0.0, abs=1e-6)


def test_all_negative_values():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [-3.0, -1.0], [-6.0, -2.0])
    assert numeric == pytest.approx(-6.000000000039306, abs=1e-6)
    assert a0 == -6.0
    assert diff == pytest.approx(3.930633596382904e-11, abs=1e-6)


def test_all_positive_values():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [2.0, 4.0], [4.0, 8.0])
    assert numeric == pytest.approx(4.000000000026205, abs=1e-6)
    assert a0 == 4.0
    assert diff == pytest.approx(2.6204816094832495e-11, abs=1e-6)


def test_singleton_boundary():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [5.0], [10.0])
    assert numeric == pytest.approx(9.999999999621423, abs=1e-6)
    assert a0 == 10.0
    assert diff == pytest.approx(3.785771696129814e-10, abs=1e-6)


def test_repeated_values():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [2.0, 2.0], [4.0, 4.0])
    assert numeric == pytest.approx(4.000000000026205, abs=1e-6)
    assert a0 == 4.0
    assert diff == pytest.approx(2.6204816094832495e-11, abs=1e-6)


def test_mixed_signs():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [-2.0, 2.0], [-4.0, 4.0])
    assert numeric == pytest.approx(-4.000000000026205, abs=1e-6)
    assert a0 == -4.0
    assert diff == pytest.approx(2.6204816094832495e-11, abs=1e-6)


def test_detects_wrong_analytic_gradient():
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), [3.0], [100.0])
    assert diff > 1.0


def test_parameter_nudge_h():
    numeric_small, _, _ = solve(lambda v: float(np.sum(v ** 2)), [3.0], [6.0], h=1e-5)
    numeric_large, _, _ = solve(lambda v: float(np.sum(v ** 2)), [3.0], [6.0], h=1e-2)
    assert numeric_small == pytest.approx(6.0, abs=1e-4)
    assert numeric_large == pytest.approx(6.0, abs=1e-2)


def test_large_n_1e5():
    x = np.ones(100000)
    numeric, a0, diff = solve(lambda v: float(np.sum(v ** 2)), x, [2.0] + [0.0] * 99999)
    assert numeric == pytest.approx(2.0, abs=1e-5)
