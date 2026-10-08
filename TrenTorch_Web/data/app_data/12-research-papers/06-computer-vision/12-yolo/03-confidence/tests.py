"""
pytest data/app_data/12-research-papers/06-computer-vision/12-yolo/03-confidence/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-yolo-confidence")
confidence = _module.confidence


def test_1_perfect_box_and_certain_object_give_one():
    assert confidence(1.0, 1.0) == 1.0


def test_2_no_object_gives_zero():
    assert confidence(0.0, 0.9) == 0.0


def test_3_zero_overlap_gives_zero():
    assert confidence(0.8, 0.0) == 0.0


def test_4_hand_value():
    assert abs(confidence(0.5, 0.4) - 0.2) < 1e-12


def test_5_stays_in_unit_interval():
    assert 0.0 <= confidence(0.3, 0.7) <= 1.0


def test_6_returns_a_python_float():
    assert isinstance(confidence(0.5, 0.5), float)

