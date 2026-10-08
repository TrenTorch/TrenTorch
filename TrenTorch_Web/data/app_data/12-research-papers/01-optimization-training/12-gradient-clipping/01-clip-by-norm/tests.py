"""
pytest data/app_data/12-research-papers/01-optimization-and-training/12-gradient-clipping/01-clip-by-norm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-by-norm")
clip_by_norm = _module.clip_by_norm


import numpy as np


def test_1_hand_case_is_rescaled():
    np.testing.assert_allclose(clip_by_norm(np.array([3.0, 4.0]), 1.0), [0.6, 0.8])


def test_2_small_gradient_unchanged():
    g = np.array([0.1, 0.2])
    np.testing.assert_allclose(clip_by_norm(g, 10.0), g)


def test_3_result_norm_equals_threshold():
    out = clip_by_norm(np.array([6.0, 8.0]), 2.0)
    assert abs(np.linalg.norm(out) - 2.0) < 1e-12


def test_4_direction_preserved():
    g = np.array([3.0, -4.0])
    out = clip_by_norm(g, 1.0)
    np.testing.assert_allclose(out / np.linalg.norm(out), g / np.linalg.norm(g))


def test_5_keeps_the_shape():
    assert clip_by_norm(np.ones((2, 2)), 0.5).shape == (2, 2)


def test_6_does_not_mutate_input():
    g = np.array([3.0, 4.0])
    clip_by_norm(g, 1.0)
    np.testing.assert_array_equal(g, [3.0, 4.0])

