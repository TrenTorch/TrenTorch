"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/06-gpipe/03-schedule-steps/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gpipe-schedule-steps")
schedule_steps = _module.schedule_steps


def test_1_four_stages_four_micro_batches_take_seven_steps():
    assert schedule_steps(4, 4) == 7


def test_2_single_stage_takes_one_step_per_micro_batch():
    assert schedule_steps(1, 5) == 5


def test_3_single_micro_batch_takes_one_step_per_stage():
    assert schedule_steps(3, 1) == 3


def test_4_more_micro_batches_add_steps_linearly():
    assert schedule_steps(4, 6) - schedule_steps(4, 5) == 1


def test_5_returns_an_integer():
    assert isinstance(schedule_steps(2, 2), int)


def test_6_consistent_with_the_bubble():
    S, M = 4, 8
    assert schedule_steps(S, M) == M + S - 1

