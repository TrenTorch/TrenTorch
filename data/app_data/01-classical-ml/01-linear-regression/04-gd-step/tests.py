"""
pytest data/01-classical-ml/01-linear-regression/04-gd-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gd_step = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}").gd_step


def test_matches_hand_computed_update():
    new_w, new_b = gd_step(np.array([1.0, 2.0]), 0.5, np.array([0.1, -0.2]), 0.05, lr=10.0)
    assert np.allclose(new_w, [0.0, 4.0])
    assert np.isclose(new_b, 0.0)


def test_zero_gradient_leaves_parameters_unchanged():
    w, b = np.array([3.0, -1.0]), 2.0
    new_w, new_b = gd_step(w, b, np.zeros(2), 0.0, lr=0.5)
    assert np.allclose(new_w, w) and np.isclose(new_b, b)


def test_does_not_mutate_input_arrays_in_place():
    # A real, common bug: modifying w in place silently corrupts the
    # caller's "before" value -- breaks any before/after comparison,
    # like the loss-decrease test in the mse-gradient question.
    w = np.array([1.0, 1.0])
    original = w.copy()
    gd_step(w, 0.0, np.array([1.0, 1.0]), 0.0, lr=1.0)
    assert np.allclose(w, original)


def test_larger_learning_rate_moves_further():
    small, _ = gd_step(np.array([0.0]), 0.0, np.array([1.0]), 0.0, lr=0.01)
    large, _ = gd_step(np.array([0.0]), 0.0, np.array([1.0]), 0.0, lr=1.0)
    assert abs(large[0]) > abs(small[0])
