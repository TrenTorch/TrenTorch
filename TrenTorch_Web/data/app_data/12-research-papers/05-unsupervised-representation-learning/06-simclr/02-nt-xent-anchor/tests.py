"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/06-simclr/02-nt-xent-anchor/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-simclr-nt-xent")
nt_xent_anchor = _module.nt_xent_anchor


import math

import numpy as np


def test_1_all_similarities_equal_gives_log_of_candidate_count():
    assert abs(nt_xent_anchor(0.5, np.array([0.5, 0.5, 0.5]), 0.7) - math.log(4.0)) < 1e-9


def test_2_dominant_positive_gives_small_loss():
    assert nt_xent_anchor(1.0, np.array([-1.0, -1.0]), 0.1) < 1e-6


def test_3_hand_value():
    # -log(e / (e + 1)) = log(1 + 1/e)
    assert abs(nt_xent_anchor(1.0, np.array([0.0]), 1.0) - math.log(1 + 1 / math.e)) < 1e-12


def test_4_lower_temperature_sharpens_the_loss():
    a = nt_xent_anchor(0.5, np.array([0.4]), 0.1)
    b = nt_xent_anchor(0.5, np.array([0.4]), 1.0)
    assert a != b


def test_5_returns_a_python_float():
    assert isinstance(nt_xent_anchor(0.1, np.array([0.2]), 0.5), float)


def test_6_more_negatives_increase_the_loss():
    a = nt_xent_anchor(0.0, np.array([0.0]), 1.0)
    b = nt_xent_anchor(0.0, np.array([0.0, 0.0, 0.0]), 1.0)
    assert b > a

