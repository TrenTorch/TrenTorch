"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/09-network-in-network/01-conv1x1/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-nin-conv1x1")
conv1x1 = _module.conv1x1


import numpy as np


def test_1_output_shape_changes_only_channels():
    out = conv1x1(np.ones((4, 5, 3)), np.ones((7, 3)), np.zeros(7))
    assert out.shape == (4, 5, 7)


def test_2_identity_weights_return_the_input():
    x = np.arange(12, dtype=float).reshape(2, 2, 3)
    np.testing.assert_allclose(conv1x1(x, np.eye(3), np.zeros(3)), x)


def test_3_bias_is_added_to_every_position():
    out = conv1x1(np.zeros((2, 2, 1)), np.ones((2, 1)), np.array([1.0, -1.0]))
    np.testing.assert_allclose(out, np.broadcast_to([1.0, -1.0], (2, 2, 2)))


def test_4_same_weights_apply_at_every_position():
    x = np.ones((3, 3, 2))
    out = conv1x1(x, np.array([[1.0, 2.0]]), np.zeros(1))
    np.testing.assert_allclose(out, np.full((3, 3, 1), 3.0))


def test_5_mixes_channels_linearly():
    x = np.array([[[1.0, 10.0]]])
    out = conv1x1(x, np.array([[1.0, 0.0], [0.0, 1.0]]), np.zeros(2))
    np.testing.assert_allclose(out, [[[1.0, 10.0]]])


def test_6_does_not_mutate_the_input():
    x = np.ones((2, 2, 2))
    conv1x1(x, np.eye(2), np.zeros(2))
    np.testing.assert_array_equal(x, np.ones((2, 2, 2)))

