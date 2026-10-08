"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/03-luong-attention/01-dot-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-luong-dot-score")
dot_score = _module.dot_score


import numpy as np


def test_1_hand_value():
    assert abs(dot_score(np.array([1.0, 2.0]), np.array([3.0, 4.0])) - 11.0) < 1e-12


def test_2_orthogonal_states_score_zero():
    assert abs(dot_score(np.array([1.0, 0.0]), np.array([0.0, 5.0]))) < 1e-12


def test_3_symmetric_in_its_arguments():
    a = np.array([1.0, -2.0])
    b = np.array([0.5, 3.0])
    assert abs(dot_score(a, b) - dot_score(b, a)) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(dot_score(np.ones(2), np.ones(2)), float)


def test_5_larger_alignment_gives_larger_score():
    assert dot_score(np.array([1.0]), np.array([2.0])) > dot_score(np.array([1.0]), np.array([1.0]))


def test_6_does_not_mutate_inputs():
    a = np.array([1.0])
    dot_score(a, np.array([2.0]))
    np.testing.assert_array_equal(a, [1.0])

