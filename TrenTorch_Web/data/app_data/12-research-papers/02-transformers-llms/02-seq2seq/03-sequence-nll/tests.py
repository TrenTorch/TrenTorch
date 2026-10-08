"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/02-seq2seq/03-sequence-nll/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-seq2seq-sequence-nll")
sequence_nll = _module.sequence_nll


import numpy as np


def test_1_uniform_distribution_gives_t_times_log_v():
    out = sequence_nll(np.full((3, 4), 0.25), np.array([0, 1, 2]))
    assert abs(out - 3 * np.log(4.0)) < 1e-9


def test_2_perfect_predictions_give_zero():
    probs = np.eye(3)
    assert abs(sequence_nll(probs, np.array([0, 1, 2]))) < 1e-12


def test_3_returns_a_python_float():
    assert isinstance(sequence_nll(np.full((2, 2), 0.5), np.array([0, 1])), float)


def test_4_matches_a_hand_computed_value():
    probs = np.array([[0.5, 0.5], [0.2, 0.8]])
    expected = -(np.log(0.5) + np.log(0.8))
    assert abs(sequence_nll(probs, np.array([0, 1])) - expected) < 1e-12


def test_5_lower_probability_gives_higher_loss():
    good = sequence_nll(np.array([[0.9, 0.1]]), np.array([0]))
    bad = sequence_nll(np.array([[0.1, 0.9]]), np.array([0]))
    assert bad > good


def test_6_does_not_mutate_inputs():
    probs = np.full((2, 2), 0.5)
    sequence_nll(probs, np.array([0, 1]))
    np.testing.assert_array_equal(probs, np.full((2, 2), 0.5))

