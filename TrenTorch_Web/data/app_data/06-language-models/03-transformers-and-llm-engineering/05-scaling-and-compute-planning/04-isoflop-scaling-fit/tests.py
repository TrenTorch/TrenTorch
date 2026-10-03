"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
import pytest

isoflop_optimum = _module.isoflop_optimum
fit_power_law = _module.fit_power_law


def test_1_recovers_the_vertex_of_an_exact_parabola():
    n = np.exp(np.linspace(1, 5, 9))
    loss = 0.3 * (np.log(n) - 3.2) ** 2 + 2.0
    assert np.isclose(isoflop_optimum(n, loss), np.exp(3.2))


def test_2_tolerates_noise():
    rng = np.random.RandomState(0)
    n = np.exp(np.linspace(1, 5, 25))
    loss = 0.3 * (np.log(n) - 3.2) ** 2 + 2.0 + rng.randn(25) * 0.005
    assert abs(np.log(isoflop_optimum(n, loss)) - 3.2) < 0.1


def test_3_monotone_curve_has_no_interior_minimum():
    n = np.exp(np.linspace(1, 5, 9))
    with pytest.raises(ValueError):
        isoflop_optimum(n, -np.log(n) ** 2)


def test_4_power_law_hand_computed():
    a, b = fit_power_law(np.array([1.0, 10.0, 100.0]), np.array([3.0, 30.0, 300.0]))
    assert np.isclose(a, 3.0) and np.isclose(b, 1.0)


def test_5_recovers_exponent_from_a_synthetic_law():
    c = np.logspace(18, 24, 7)
    n = 0.09 * c ** 0.5
    a, b = fit_power_law(c, n)
    assert np.isclose(a, 0.09) and np.isclose(b, 0.5)


def test_6_extrapolation_from_the_fit():
    c = np.logspace(18, 21, 4)
    a, b = fit_power_law(c, 0.1 * c ** 0.48)
    assert np.isclose(a * 1e24 ** b, 0.1 * 1e24 ** 0.48, rtol=1e-6)


def test_7_full_pipeline_and_inputs_untouched():
    budgets = np.array([1e18, 1e19, 1e20])
    optimal = []
    for C in budgets:
        n = np.exp(np.linspace(np.log(1e6), np.log(1e10), 15))
        center = np.log(0.1 * C ** 0.5)
        loss = 0.2 * (np.log(n) - center) ** 2 + 1.5
        snap = n.copy()
        optimal.append(isoflop_optimum(n, loss))
        assert np.array_equal(n, snap)
    _, b = fit_power_law(budgets, np.array(optimal))
    assert np.isclose(b, 0.5, atol=1e-6)
