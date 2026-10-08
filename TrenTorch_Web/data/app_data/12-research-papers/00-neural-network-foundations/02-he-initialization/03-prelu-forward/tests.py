"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/02-he-initialization/03-prelu-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-prelu-forward")
prelu = _module.prelu


import numpy as np


def test_1_positive_inputs_pass_through():
    np.testing.assert_allclose(prelu(np.array([1.0, 2.5]), 0.25), [1.0, 2.5])


def test_2_negative_inputs_are_scaled_by_a():
    np.testing.assert_allclose(prelu(np.array([-2.0, -4.0]), 0.25), [-0.5, -1.0])


def test_3_a_zero_reduces_to_relu():
    x = np.array([-3.0, 0.0, 3.0])
    np.testing.assert_allclose(prelu(x, 0.0), [0.0, 0.0, 3.0])


def test_4_zero_input_is_zero():
    assert prelu(np.array([0.0]), 0.5)[0] == 0.0


def test_5_keeps_the_input_shape():
    out = prelu(np.ones((2, 3)) * -1, 0.1)
    assert out.shape == (2, 3)


def test_6_does_not_mutate_the_input():
    x = np.array([-1.0, 2.0])
    prelu(x, 0.3)
    np.testing.assert_array_equal(x, [-1.0, 2.0])

