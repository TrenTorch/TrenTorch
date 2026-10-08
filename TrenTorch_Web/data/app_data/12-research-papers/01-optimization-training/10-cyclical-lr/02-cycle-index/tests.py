"""
pytest data/app_data/12-research-papers/01-optimization-and-training/10-cyclical-lr/02-cycle-index/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clr-cycle-index")
cycle_index = _module.cycle_index


import math


def test_1_first_cycle_at_start():
    assert cycle_index(0, 4) == 1


def test_2_hand_case():
    assert cycle_index(10, 4) == 2


def test_3_second_cycle_begins_at_two_steps():
    assert cycle_index(8, 4) == 2


def test_4_returns_an_integer():
    assert isinstance(cycle_index(5, 3), int)


def test_5_increases_with_iteration():
    assert cycle_index(100, 4) > cycle_index(10, 4)


def test_6_matches_floor_definition():
    assert cycle_index(17, 5) == math.floor(1 + 17 / 10)

