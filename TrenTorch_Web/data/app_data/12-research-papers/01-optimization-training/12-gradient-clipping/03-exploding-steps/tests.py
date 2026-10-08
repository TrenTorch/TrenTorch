"""
pytest data/app_data/12-research-papers/01-optimization-and-training/12-gradient-clipping/03-exploding-steps/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-exploding-steps")
exploding_steps = _module.exploding_steps


def test_1_hand_case():
    assert exploding_steps([0.5, 3.0, 2.5, 1.0], 2.0) == 2


def test_2_none_exceed():
    assert exploding_steps([0.1, 0.2], 1.0) == 0


def test_3_equal_to_threshold_is_not_counted():
    assert exploding_steps([2.0], 2.0) == 0


def test_4_all_exceed():
    assert exploding_steps([5.0, 6.0, 7.0], 1.0) == 3


def test_5_returns_an_integer():
    assert isinstance(exploding_steps([3.0], 1.0), int)


def test_6_empty_history_is_zero():
    assert exploding_steps([], 1.0) == 0

