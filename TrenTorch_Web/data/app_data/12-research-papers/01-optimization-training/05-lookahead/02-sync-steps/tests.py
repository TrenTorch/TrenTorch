"""
pytest data/app_data/12-research-papers/01-optimization-and-training/05-lookahead/02-sync-steps/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lookahead-sync-steps")
sync_steps = _module.sync_steps


def test_1_hand_case():
    assert sync_steps(7, 3) == [3, 6]


def test_2_k_one_syncs_every_step():
    assert sync_steps(4, 1) == [1, 2, 3, 4]


def test_3_k_larger_than_total_gives_none():
    assert sync_steps(5, 10) == []


def test_4_last_step_syncs_when_divisible():
    assert sync_steps(6, 2)[-1] == 6


def test_5_count_is_floor_of_total_over_k():
    assert len(sync_steps(20, 4)) == 5


def test_6_returns_a_list_of_ints():
    assert all(isinstance(s, int) for s in sync_steps(9, 3))

