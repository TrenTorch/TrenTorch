"""
pytest data/app_data/12-research-papers/01-optimization-and-training/06-adafactor/03-relative-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adafactor-relative-step")
relative_step = _module.relative_step


import math


def test_1_first_step_is_capped():
    assert abs(relative_step(1) - 0.01) < 1e-12


def test_2_decays_after_the_cap():
    assert abs(relative_step(40000) - 0.005) < 1e-12


def test_3_boundary_at_ten_thousand():
    assert abs(relative_step(10000) - 0.01) < 1e-12


def test_4_is_nonincreasing():
    assert relative_step(100) >= relative_step(10000)


def test_5_returns_a_float():
    assert isinstance(relative_step(3), float)


def test_6_matches_definition():
    assert abs(relative_step(25) - min(0.01, 1 / math.sqrt(25))) < 1e-12

