"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/08-temporal-convolutional-networks/01-tcn-receptive-field/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tcn-receptive-field")
tcn_receptive_field = _module.tcn_receptive_field


def test_1_three_levels_kernel_two_sees_eight():
    assert tcn_receptive_field(2, 3) == 8


def test_2_zero_levels_sees_one_step():
    assert tcn_receptive_field(3, 0) == 1


def test_3_kernel_three_one_level_sees_three():
    assert tcn_receptive_field(3, 1) == 3


def test_4_grows_exponentially_with_levels():
    assert tcn_receptive_field(2, 6) > tcn_receptive_field(2, 3) * 4


def test_5_returns_an_integer():
    assert isinstance(tcn_receptive_field(2, 2), int)


def test_6_matches_the_explicit_sum():
    k, L = 3, 4
    assert tcn_receptive_field(k, L) == 1 + sum((k - 1) * 2**i for i in range(L))

