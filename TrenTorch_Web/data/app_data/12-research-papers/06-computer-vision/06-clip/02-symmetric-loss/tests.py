"""
pytest data/app_data/12-research-papers/06-computer-vision/06-clip/02-symmetric-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-symmetric-loss")
clip_symmetric_loss = _module.clip_symmetric_loss


import math

import numpy as np


def test_1_uniform_logits_give_log_n():
    assert abs(clip_symmetric_loss(np.zeros((4, 4))) - math.log(4.0)) < 1e-9


def test_2_dominant_diagonal_gives_small_loss():
    L = np.eye(3) * 50.0
    assert clip_symmetric_loss(L) < 1e-6


def test_3_is_symmetric_under_transpose():
    rng = np.random.default_rng(0)
    L = rng.normal(size=(5, 5))
    assert abs(clip_symmetric_loss(L) - clip_symmetric_loss(L.T)) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(clip_symmetric_loss(np.zeros((2, 2))), float)


def test_5_wrong_diagonal_gives_large_loss():
    L = np.zeros((3, 3))
    L[0, 0] = -50.0
    L[1, 1] = 50.0
    assert clip_symmetric_loss(L) > 1.0


def test_6_does_not_mutate_logits():
    L = np.eye(2)
    clip_symmetric_loss(L)
    np.testing.assert_array_equal(L, np.eye(2))

