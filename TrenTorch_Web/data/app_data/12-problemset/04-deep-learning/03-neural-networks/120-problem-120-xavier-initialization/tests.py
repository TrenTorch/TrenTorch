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
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_02_exact_zero_inputs():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_03_all_negative_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_04_all_positive_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_05_singleton_boundary():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_06_repeated_values():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_07_mixed_signs():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_08_tiny_magnitudes():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_09_large_magnitudes():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_10_parameter_nudge():
    args = [3, 4, 1]
    actual = solve(*args)
    expected = np.array([[0.021889395518930654, 0.8340966885527794, -0.6588883657100241, 0.8307373518230063], [-0.348420447747417, -0.14197182932425167, 0.6067872962131307, -0.1681305292522739], [0.09182966573912132, -0.8747905378278702, 0.46941506313391823, 0.07062769210065567]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)

def test_11_reversed_order():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)


def test_13_empty_or_degenerate_input():
    args = [2, 3, 0]
    actual = solve(*args)
    expected = np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]], dtype=float)
    np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=1e-6, equal_nan=True)
