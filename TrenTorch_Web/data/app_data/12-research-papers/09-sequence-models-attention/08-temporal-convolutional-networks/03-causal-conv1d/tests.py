"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/08-temporal-convolutional-networks/03-causal-conv1d/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tcn-causal-conv1d")
causal_conv1d = _module.causal_conv1d


import numpy as np


def test_1_identity_kernel_returns_the_input():
    np.testing.assert_allclose(causal_conv1d(np.array([1.0, 2.0, 3.0]), np.array([1.0, 0.0])), [1.0, 2.0, 3.0])


def test_2_hand_value_with_two_taps():
    np.testing.assert_allclose(causal_conv1d(np.array([1.0, 2.0, 3.0]), np.array([1.0, 1.0])), [1.0, 3.0, 5.0])


def test_3_second_tap_delays_the_signal():
    np.testing.assert_allclose(causal_conv1d(np.array([1.0, 2.0, 3.0]), np.array([0.0, 1.0])), [0.0, 1.0, 2.0])


def test_4_output_is_causal():
    x = np.array([0.0, 0.0, 5.0, 0.0])
    out = causal_conv1d(x, np.array([1.0, 1.0]))
    assert out[1] == 0.0


def test_5_output_length_matches_input():
    assert len(causal_conv1d(np.ones(7), np.ones(3))) == 7


def test_6_does_not_mutate_input():
    x = np.array([1.0, 2.0])
    causal_conv1d(x, np.array([1.0]))
    np.testing.assert_array_equal(x, [1.0, 2.0])

