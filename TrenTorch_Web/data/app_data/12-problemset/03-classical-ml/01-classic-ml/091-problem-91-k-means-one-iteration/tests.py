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
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_02_exact_zero_inputs():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_03_all_negative_values():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_04_all_positive_values():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_05_singleton_boundary():
    args = [[[0.0, 0.0]], [[0.0, 0.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_06_repeated_values():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_07_mixed_signs():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_08_tiny_magnitudes():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_09_large_magnitudes():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_10_parameter_nudge():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_11_reversed_order():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)

def test_12_large_n_1e5():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(NameError):
        solve(*args)

def test_13_empty_or_degenerate_input():
    args = [[[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]]]
    with pytest.raises(TypeError):
        solve(*args)
