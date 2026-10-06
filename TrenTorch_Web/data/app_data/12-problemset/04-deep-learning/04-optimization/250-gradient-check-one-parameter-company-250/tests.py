"""Executable tests: 2 visible examples + 11 targeted edge/performance cases.

The case names document the hidden-test categories. Expected values are materialized
from the reference implementation at authoring time; the agent should not have to
invent edge cases or expected outputs.
"""
import numpy as np
import pytest
from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve

def test_01_basic_example():
    args = [np.array([1.0, -1.0, 2.0], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float), np.array([1.0], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_02_exact_zero_inputs():
    args = [np.array([0.0, 0.0, 0.0], dtype=float), np.array([0.0, 0.0, 0.0], dtype=float), np.array([0.0], dtype=float), np.array([0.0, 0.0, 0.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_03_all_negative_values():
    args = [np.array([-2.0, -2.0, -3.0], dtype=float), np.array([-2.0, -2.0, -3.0], dtype=float), np.array([-2.0], dtype=float), np.array([-2.0, -2.0, -3.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_04_all_positive_values():
    args = [np.array([2.0, 2.0, 3.0], dtype=float), np.array([2.0, 2.0, 3.0], dtype=float), np.array([2.0], dtype=float), np.array([2.0, 2.0, 3.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_05_singleton_boundary():
    args = [np.array([1.0], dtype=float), np.array([1.0], dtype=float), np.array([1.0], dtype=float), np.array([1.0], dtype=float)]
    with pytest.raises(TypeError):
        solve(*args)

def test_06_repeated_values():
    args = [np.array([2.0, 2.0, 2.0], dtype=float), np.array([2.0, 2.0, 2.0], dtype=float), np.array([2.0], dtype=float), np.array([2.0, 2.0, 2.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_07_mixed_signs():
    args = [np.array([-2.0, 0.0, 2.0], dtype=float), np.array([-2.0, 0.0, 2.0], dtype=float), np.array([-2.0], dtype=float), np.array([-2.0, 0.0, 2.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_08_tiny_magnitudes():
    args = [np.array([1e-08, 1e-08, 1e-08], dtype=float), np.array([1e-08, 1e-08, 1e-08], dtype=float), np.array([1e-08], dtype=float), np.array([1e-08, 1e-08, 1e-08], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_09_large_magnitudes():
    args = [np.array([1000.0, 1000.0, 1000.0], dtype=float), np.array([1000.0, 1000.0, 1000.0], dtype=float), np.array([1000.0], dtype=float), np.array([1000.0, 1000.0, 1000.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_10_parameter_nudge():
    args = [np.array([1.0, -1.0, 2.0], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float), np.array([1.0], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

def test_11_reversed_order():
    args = [np.array([2.0, -1.0, 1.0], dtype=float), np.array([2.0, -1.0, 1.0], dtype=float), np.array([1.0], dtype=float), np.array([2.0, -1.0, 1.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)

@pytest.mark.skip(reason="Not applicable: the 1e5-row case needs arguments that share one row dimension")
def test_12_large_n_1e5():
    pass

def test_13_empty_or_degenerate_input():
    args = [np.array([], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float), np.array([1.0], dtype=float), np.array([1.0, -1.0, 2.0], dtype=float)]
    with pytest.raises(ValueError):
        solve(*args)
