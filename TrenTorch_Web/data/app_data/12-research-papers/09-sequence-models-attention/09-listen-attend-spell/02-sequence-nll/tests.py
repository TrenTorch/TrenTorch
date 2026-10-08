"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/09-listen-attend-spell/02-sequence-nll/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-las-sequence-nll")
char_nll = _module.char_nll


import numpy as np


def test_1_uniform_over_four_characters():
    lp = np.full((3, 4), np.log(0.25))
    assert abs(char_nll(lp, np.array([0, 1, 2])) - 3 * np.log(4.0)) < 1e-9


def test_2_perfect_prediction_gives_zero():
    lp = np.log(np.eye(2) + 1e-300)
    assert abs(char_nll(lp, np.array([0, 1]))) < 1e-9


def test_3_returns_a_python_float():
    assert isinstance(char_nll(np.zeros((1, 2)), np.array([0])), float)


def test_4_hand_value():
    lp = np.log(np.array([[0.5, 0.5], [0.2, 0.8]]))
    assert abs(char_nll(lp, np.array([0, 1])) - (-(np.log(0.5) + np.log(0.8)))) < 1e-12


def test_5_longer_transcripts_have_larger_totals():
    lp = np.log(np.full((4, 2), 0.5))
    assert char_nll(lp, np.zeros(4, dtype=int)) > char_nll(lp[:2], np.zeros(2, dtype=int))


def test_6_does_not_mutate_inputs():
    lp = np.log(np.full((2, 2), 0.5))
    char_nll(lp, np.array([0, 1]))
    np.testing.assert_allclose(lp, np.log(np.full((2, 2), 0.5)))

