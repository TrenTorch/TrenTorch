"""Executable tests: 2 visible examples + 11 targeted edge/performance cases.

The case names document the hidden-test categories. Expected values are materialized
from the reference implementation at authoring time; the agent should not have to
invent edge cases or expected outputs.
"""
import numpy as np
from numpy import nan
import pytest
from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve

def test_01_basic_example():
    args = [[2.0, 3.0], [1.0, -1.0]]
    actual = solve(*args)
    expected = -0.7071067811865475
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_02_exact_zero_inputs():
    args = [[0, 0], [0, 0]]
    actual = solve(*args)
    assert np.isnan(actual)

def test_03_all_negative_values():
    args = [[-3.0, -4.0], [-2.0, -2.0]]
    actual = solve(*args)
    expected = 4.949747468305832
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_04_all_positive_values():
    args = [[3.0, 4.0], [2.0, 2.0]]
    actual = solve(*args)
    expected = 4.949747468305832
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_05_singleton_boundary():
    args = [[2.0], [1.0]]
    actual = solve(*args)
    expected = 2.0
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_06_repeated_values():
    args = [[2, 2], [2, 2]]
    actual = solve(*args)
    expected = 2.82842712474619
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_07_mixed_signs():
    args = [[-2.0, 2.0], [-2.0, 2.0]]
    actual = solve(*args)
    expected = 2.82842712474619
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_08_tiny_magnitudes():
    args = [[1e-08, 1e-08], [1e-08, 1e-08]]
    actual = solve(*args)
    expected = 1.414213562373095e-08
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_09_large_magnitudes():
    args = [[1000.0, 1000.0], [1000.0, 1000.0]]
    actual = solve(*args)
    expected = 1414.2135623730949
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_10_parameter_nudge():
    args = [[2.0, 3.0], [1.0, -1.0]]
    actual = solve(*args)
    expected = -0.7071067811865475
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

def test_11_reversed_order():
    args = [[3.0, 2.0], [-1.0, 1.0]]
    actual = solve(*args)
    expected = -0.7071067811865475
    assert actual == pytest.approx(expected, abs=1e-6, rel=1e-6) if isinstance(expected, (float, np.floating)) else actual == expected

@pytest.mark.skip(reason="Not applicable: the 1e5-row case needs arguments that share one row dimension")
def test_12_large_n_1e5():
    pass

def test_13_empty_or_degenerate_input():
    args = [[], [1.0, -1.0]]
    with pytest.raises(ValueError):
        solve(*args)
