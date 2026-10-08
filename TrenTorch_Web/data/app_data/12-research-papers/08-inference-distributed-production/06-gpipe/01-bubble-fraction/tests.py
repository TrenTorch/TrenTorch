"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/06-gpipe/01-bubble-fraction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gpipe-bubble-fraction")
pipeline_bubble_fraction = _module.pipeline_bubble_fraction


def test_1_single_stage_has_no_bubble():
    assert pipeline_bubble_fraction(1, 8) == 0.0


def test_2_hand_value_four_stages_four_micro_batches():
    assert abs(pipeline_bubble_fraction(4, 4) - 3 / 7) < 1e-12


def test_3_more_micro_batches_shrink_the_bubble():
    assert pipeline_bubble_fraction(4, 16) < pipeline_bubble_fraction(4, 4)


def test_4_bubble_is_below_one():
    assert 0.0 <= pipeline_bubble_fraction(8, 2) < 1.0


def test_5_returns_a_float():
    assert isinstance(pipeline_bubble_fraction(2, 2), float)


def test_6_matches_idle_slots_over_total_slots():
    S, M = 3, 5
    total = M + S - 1
    assert abs(pipeline_bubble_fraction(S, M) - (S - 1) / total) < 1e-12

