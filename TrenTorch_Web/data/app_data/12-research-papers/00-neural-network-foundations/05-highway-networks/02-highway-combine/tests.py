"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/05-highway-networks/02-highway-combine/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-highway-combine")
highway_combine = _module.highway_combine


import numpy as np


def test_1_gate_zero_returns_the_input():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(highway_combine(x, np.array([9.0, 9.0]), np.zeros(2)), x)


def test_2_gate_one_returns_the_transform():
    h = np.array([3.0, 4.0])
    np.testing.assert_allclose(highway_combine(np.zeros(2), h, np.ones(2)), h)


def test_3_gate_half_averages_the_two_paths():
    out = highway_combine(np.array([2.0]), np.array([4.0]), np.array([0.5]))
    np.testing.assert_allclose(out, [3.0])


def test_4_each_feature_uses_its_own_gate():
    out = highway_combine(np.array([1.0, 1.0]), np.array([5.0, 5.0]), np.array([1.0, 0.0]))
    np.testing.assert_allclose(out, [5.0, 1.0])


def test_5_keeps_the_input_shape():
    assert highway_combine(np.ones((2, 3)), np.ones((2, 3)), np.ones((2, 3))).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    x = np.array([1.0])
    highway_combine(x, np.array([2.0]), np.array([0.5]))
    np.testing.assert_array_equal(x, [1.0])

