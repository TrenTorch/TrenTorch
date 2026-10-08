"""
pytest data/app_data/12-research-papers/01-optimization-and-training/11-sgdr/02-cycle-position/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sgdr-cycle-position")
sgdr_position = _module.sgdr_position


def test_1_inside_first_cycle():
    assert sgdr_position(5, 10, 2) == (5, 10)


def test_2_hand_case_after_restart():
    assert sgdr_position(12, 10, 2) == (2, 20)


def test_3_exact_restart_point():
    assert sgdr_position(10, 10, 2) == (0, 20)


def test_4_multiple_restarts():
    assert sgdr_position(35, 10, 2) == (5, 40)


def test_5_tmult_one_gives_fixed_cycles():
    assert sgdr_position(25, 10, 1) == (5, 10)


def test_6_returns_a_tuple_of_ints():
    t, T = sgdr_position(7, 3, 2)
    assert isinstance(t, int) and isinstance(T, int)

