"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/10-maxout-networks/03-relu-as-maxout/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-maxout-relu")
relu_via_maxout = _module.relu_via_maxout


import numpy as np


def test_1_positive_values_pass_through():
    np.testing.assert_allclose(relu_via_maxout(np.array([1.0, 2.5])), [1.0, 2.5])


def test_2_negative_values_become_zero():
    np.testing.assert_allclose(relu_via_maxout(np.array([-1.0, -3.0])), [0.0, 0.0])


def test_3_zero_stays_zero():
    assert relu_via_maxout(np.array([0.0]))[0] == 0.0


def test_4_keeps_array_shape():
    assert relu_via_maxout(np.ones((2, 3))).shape == (2, 3)


def test_5_matches_numpy_maximum_with_zero():
    rng = np.random.default_rng(0)
    x = rng.normal(size=50)
    np.testing.assert_allclose(relu_via_maxout(x), np.maximum(x, 0.0))


def test_6_does_not_mutate_input():
    x = np.array([-1.0, 1.0])
    relu_via_maxout(x)
    np.testing.assert_array_equal(x, [-1.0, 1.0])

