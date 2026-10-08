"""
pytest data/app_data/12-research-papers/06-computer-vision/11-squeeze-excitation/02-excitation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-se-excitation")
excitation = _module.excitation


import numpy as np


def test_1_zero_weights_give_half_gates():
    out = excitation(np.ones(4), np.zeros((2, 4)), np.zeros((4, 2)))
    np.testing.assert_allclose(out, [0.5] * 4)


def test_2_gates_lie_strictly_between_zero_and_one():
    rng = np.random.default_rng(0)
    out = excitation(rng.normal(size=6), rng.normal(size=(3, 6)), rng.normal(size=(6, 3)))
    assert np.all(out > 0) and np.all(out < 1)


def test_3_output_length_matches_channels():
    assert excitation(np.ones(8), np.ones((2, 8)), np.ones((8, 2))).shape == (8,)


def test_4_hand_value_with_identity_like_weights():
    out = excitation(np.array([1.0]), np.array([[1.0]]), np.array([[0.0]]))
    np.testing.assert_allclose(out, [0.5])


def test_5_negative_summary_is_suppressed_by_relu_bottleneck():
    out = excitation(np.array([-5.0]), np.array([[1.0]]), np.array([[10.0]]))
    np.testing.assert_allclose(out, [0.5], atol=1e-9)


def test_6_does_not_mutate_inputs():
    s = np.array([1.0, 2.0])
    excitation(s, np.ones((1, 2)), np.ones((2, 1)))
    np.testing.assert_array_equal(s, [1.0, 2.0])

