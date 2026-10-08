"""
pytest data/app_data/12-research-papers/01-optimization-and-training/05-lookahead/03-slow-trajectory/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lookahead-trajectory")
slow_trajectory = _module.slow_trajectory


def test_1_hand_case():
    out = slow_trajectory(0.0, [1.0, 1.0], 0.5)
    assert abs(out[0] - 0.5) < 1e-12 and abs(out[1] - 0.75) < 1e-12


def test_2_length_matches_sync_count():
    assert len(slow_trajectory(0.0, [1.0, 2.0, 3.0], 0.5)) == 3


def test_3_alpha_one_tracks_fast_points():
    assert slow_trajectory(0.0, [2.0, 5.0], 1.0) == [2.0, 5.0]


def test_4_alpha_zero_stays_at_start():
    assert slow_trajectory(7.0, [1.0, 2.0], 0.0) == [7.0, 7.0]


def test_5_slow_weight_is_carried_forward():
    out = slow_trajectory(0.0, [4.0, 4.0], 0.25)
    assert abs(out[1] - (out[0] + 0.25 * (4.0 - out[0]))) < 1e-12


def test_6_empty_input_gives_empty_output():
    assert slow_trajectory(0.0, [], 0.5) == []

