"""
pytest data/app_data/12-research-papers/01-optimization-and-training/11-sgdr/01-cosine-lr/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sgdr-cosine-lr")
cosine_lr = _module.cosine_lr


import math


def test_1_starts_at_max():
    assert abs(cosine_lr(0, 10, 0.0, 1.0) - 1.0) < 1e-12


def test_2_halfway_is_midpoint():
    assert abs(cosine_lr(5, 10, 0.0, 1.0) - 0.5) < 1e-12


def test_3_end_of_cycle_is_min():
    assert abs(cosine_lr(10, 10, 0.0, 1.0)) < 1e-12


def test_4_is_nonincreasing_within_cycle():
    vals = [cosine_lr(t, 10, 0.0, 1.0) for t in range(11)]
    assert all(b <= a + 1e-12 for a, b in zip(vals, vals[1:]))


def test_5_respects_nonzero_minimum():
    assert abs(cosine_lr(10, 10, 0.2, 1.0) - 0.2) < 1e-12


def test_6_matches_formula():
    assert abs(cosine_lr(3, 8, 0.1, 0.9) - (0.1 + 0.5 * 0.8 * (1 + math.cos(math.pi * 3 / 8)))) < 1e-12

