"""
pytest data/app_data/12-research-papers/06-computer-vision/11-squeeze-excitation/03-recalibrate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-se-recalibrate")
recalibrate = _module.recalibrate


import numpy as np


def test_1_unit_gates_keep_the_features():
    x = np.arange(8.0).reshape(2, 2, 2)
    np.testing.assert_allclose(recalibrate(x, np.ones(2)), x)


def test_2_zero_gate_silences_a_channel():
    out = recalibrate(np.ones((2, 2, 2)), np.array([0.0, 1.0]))
    np.testing.assert_allclose(out[:, :, 0], 0.0)


def test_3_gate_scales_its_channel():
    out = recalibrate(np.ones((1, 1, 2)), np.array([0.5, 3.0]))
    np.testing.assert_allclose(out, [[[0.5, 3.0]]])


def test_4_keeps_the_shape():
    assert recalibrate(np.ones((3, 4, 5)), np.ones(5)).shape == (3, 4, 5)


def test_5_gate_applies_to_every_spatial_position():
    out = recalibrate(np.ones((2, 2, 1)), np.array([2.0]))
    np.testing.assert_allclose(out, np.full((2, 2, 1), 2.0))


def test_6_does_not_mutate_input():
    x = np.ones((1, 1, 1))
    recalibrate(x, np.array([5.0]))
    np.testing.assert_array_equal(x, np.ones((1, 1, 1)))

