"""
pytest data/app_data/12-research-papers/01-optimization-and-training/08-sophia/01-clipped-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sophia-clipped-step")
sophia_step = _module.sophia_step


import numpy as np


def test_1_hand_case_with_clipping():
    out = sophia_step(np.array([1.0, -10.0]), np.array([1.0, 1.0]), 0.5, 1e-8)
    np.testing.assert_allclose(out, [1.0, -1.0])


def test_2_small_steps_are_not_clipped():
    out = sophia_step(np.array([0.1]), np.array([1.0]), 1.0, 1e-8)
    np.testing.assert_allclose(out, [0.1])


def test_3_entries_stay_within_unit_interval():
    out = sophia_step(np.array([100.0, -100.0, 0.2]), np.array([0.01, 0.01, 1.0]), 1.0, 1e-8)
    assert np.all(np.abs(out) <= 1.0)


def test_4_floor_prevents_division_by_zero():
    out = sophia_step(np.array([1e-6]), np.array([0.0]), 1.0, 1e-3)
    assert np.isfinite(out[0])


def test_5_keeps_the_shape():
    assert sophia_step(np.ones((2, 2)), np.ones((2, 2)), 1.0, 1e-8).shape == (2, 2)


def test_6_does_not_mutate_momentum():
    m = np.array([1.0])
    sophia_step(m, np.array([1.0]), 1.0, 1e-8)
    np.testing.assert_array_equal(m, [1.0])

