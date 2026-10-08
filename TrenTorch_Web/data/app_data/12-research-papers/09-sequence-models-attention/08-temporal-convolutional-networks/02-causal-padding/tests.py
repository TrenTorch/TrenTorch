"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/08-temporal-convolutional-networks/02-causal-padding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tcn-causal-padding")
causal_padding = _module.causal_padding


def test_1_kernel_three_dilation_two_pads_four():
    assert causal_padding(3, 2) == 4


def test_2_kernel_one_needs_no_padding():
    assert causal_padding(1, 8) == 0


def test_3_dilation_one_pads_kernel_minus_one():
    assert causal_padding(5, 1) == 4


def test_4_padding_grows_with_dilation():
    assert causal_padding(2, 4) > causal_padding(2, 2)


def test_5_returns_an_integer():
    assert isinstance(causal_padding(2, 2), int)


def test_6_zero_dilation_is_no_padding():
    assert causal_padding(3, 0) == 0

