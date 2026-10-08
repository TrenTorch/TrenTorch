"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/07-wavenet/01-receptive-field/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-wavenet-receptive-field")
wavenet_receptive_field = _module.wavenet_receptive_field


def test_1_one_layer_kernel_two_sees_two_samples():
    assert wavenet_receptive_field([1], 2) == 2


def test_2_dilations_one_to_eight_give_sixteen():
    assert wavenet_receptive_field([1, 2, 4, 8], 2) == 16


def test_3_no_layers_sees_one_sample():
    assert wavenet_receptive_field([], 2) == 1


def test_4_larger_kernel_grows_the_field():
    assert wavenet_receptive_field([1, 2], 3) > wavenet_receptive_field([1, 2], 2)


def test_5_returns_an_integer():
    assert isinstance(wavenet_receptive_field([1], 2), int)


def test_6_doubling_dilations_grows_exponentially():
    assert wavenet_receptive_field([1, 2, 4, 8, 16], 2) == 32

