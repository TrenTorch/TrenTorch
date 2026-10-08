"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/12-s4/02-causal-conv/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-s4-causal-conv")
causal_conv_from_kernel = _module.causal_conv_from_kernel


def test_1_kernel_of_ones_gives_running_sum():
    assert causal_conv_from_kernel([1.0, 1.0], [1.0, 2.0, 3.0]) == [1.0, 3.0, 5.0]


def test_2_identity_kernel_returns_input():
    assert causal_conv_from_kernel([1.0], [4.0, 5.0]) == [4.0, 5.0]


def test_3_output_is_causal():
    assert causal_conv_from_kernel([1.0, 1.0], [0.0, 0.0, 9.0])[1] == 0.0


def test_4_output_length_matches_input():
    assert len(causal_conv_from_kernel([1.0, 0.5], [1.0, 1.0, 1.0, 1.0])) == 4


def test_5_longer_kernel_than_input_is_handled():
    out = causal_conv_from_kernel([1.0, 1.0, 1.0], [2.0])
    assert out == [2.0]


def test_6_does_not_mutate_inputs():
    x = [1.0, 2.0]
    causal_conv_from_kernel([1.0], x)
    assert x == [1.0, 2.0]

