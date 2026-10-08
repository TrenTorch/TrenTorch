"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/12-glow/02-logdet-1x1/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-glow-logdet-1x1")
logdet_1x1 = _module.logdet_1x1


import math

import numpy as np


def test_1_identity_has_zero_logdet():
    assert abs(logdet_1x1(np.eye(3), 4, 4)) < 1e-12


def test_2_scaled_identity_matches_hand_value():
    # det(2 I_2) = 4, log 4 per position, 2 * 3 positions
    assert abs(logdet_1x1(2 * np.eye(2), 2, 3) - 6 * math.log(4.0)) < 1e-9


def test_3_diagonal_matrix_adds_log_of_entries():
    assert abs(logdet_1x1(np.diag([2.0, 3.0]), 1, 1) - math.log(6.0)) < 1e-9


def test_4_scales_with_spatial_size():
    assert abs(logdet_1x1(np.diag([2.0]), 4, 4) - 16 * math.log(2.0)) < 1e-9


def test_5_returns_a_python_float():
    assert isinstance(logdet_1x1(np.eye(2), 1, 1), float)


def test_6_does_not_mutate_weights():
    W = np.diag([2.0, 2.0])
    logdet_1x1(W, 1, 1)
    np.testing.assert_array_equal(W, np.diag([2.0, 2.0]))

