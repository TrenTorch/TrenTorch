"""
pytest data/app_data/12-research-papers/01-optimization-and-training/10-cyclical-lr/01-triangular-lr/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clr-triangular-lr")
triangular_lr = _module.triangular_lr


import math


def test_1_starts_at_base():
    assert abs(triangular_lr(0, 0.1, 0.5, 4) - 0.1) < 1e-12


def test_2_midway_up_is_halfway():
    assert abs(triangular_lr(2, 0.1, 0.5, 4) - 0.3) < 1e-12


def test_3_peaks_at_max_at_half_cycle():
    assert abs(triangular_lr(4, 0.1, 0.5, 4) - 0.5) < 1e-12


def test_4_returns_to_base_at_full_cycle():
    assert abs(triangular_lr(8, 0.1, 0.5, 4) - 0.1) < 1e-12


def test_5_stays_between_bounds():
    vals = [triangular_lr(i, 0.1, 0.5, 4) for i in range(40)]
    assert all(0.1 - 1e-12 <= v <= 0.5 + 1e-12 for v in vals)


def test_6_matches_definition_for_arbitrary_iteration():
    it, base, mx, s = 3, 0.2, 1.0, 5
    cycle = math.floor(1 + it / (2 * s))
    x = abs(it / s - 2 * cycle + 1)
    assert abs(triangular_lr(it, base, mx, s) - (base + (mx - base) * max(0.0, 1 - x))) < 1e-12

