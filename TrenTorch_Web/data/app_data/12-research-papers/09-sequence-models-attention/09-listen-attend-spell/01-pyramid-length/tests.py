"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/09-listen-attend-spell/01-pyramid-length/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-las-pyramid-length")
pyramid_length = _module.pyramid_length


import math


def test_1_two_layers_quarter_the_length():
    assert pyramid_length(8, 2) == 2


def test_2_zero_layers_keep_the_length():
    assert pyramid_length(7, 0) == 7


def test_3_rounds_up_for_odd_lengths():
    assert pyramid_length(5, 1) == 3


def test_4_returns_an_integer():
    assert isinstance(pyramid_length(9, 2), int)


def test_5_more_layers_shorter_sequence():
    assert pyramid_length(64, 3) < pyramid_length(64, 2)


def test_6_matches_repeated_halving():
    n = 37
    for _ in range(3):
        n = math.ceil(n / 2)
    assert pyramid_length(37, 3) == n

