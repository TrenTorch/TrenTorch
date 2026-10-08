"""
pytest data/app_data/12-research-papers/01-optimization-and-training/08-sophia/03-clip-fraction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sophia-clip-fraction")
clip_fraction = _module.clip_fraction


import numpy as np


def test_1_hand_case():
    assert abs(clip_fraction(np.array([2.0, -0.5, 0.3, -5.0])) - 0.5) < 1e-12


def test_2_nothing_clipped_gives_zero():
    assert clip_fraction(np.array([0.1, -0.2])) == 0.0


def test_3_everything_clipped_gives_one():
    assert clip_fraction(np.array([1.0, -3.0])) == 1.0


def test_4_boundary_counts_as_clipped():
    assert clip_fraction(np.array([1.0])) == 1.0


def test_5_returns_a_float_in_unit_interval():
    f = clip_fraction(np.array([0.5, 2.0, 0.1]))
    assert isinstance(f, float) and 0.0 <= f <= 1.0


def test_6_sign_does_not_matter():
    assert clip_fraction(np.array([-2.0])) == clip_fraction(np.array([2.0]))

