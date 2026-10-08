"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/06-memory-networks/01-memory-match/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-memnet-match")
memory_match = _module.memory_match


import numpy as np


def test_1_hand_value_per_memory():
    np.testing.assert_allclose(memory_match(np.array([1.0, 0.0]), np.array([[2.0, 5.0], [0.0, 3.0]])), [2.0, 0.0])


def test_2_one_score_per_memory():
    assert memory_match(np.ones(3), np.ones((4, 3))).shape == (4,)


def test_3_orthogonal_memory_scores_zero():
    assert memory_match(np.array([1.0, 0.0]), np.array([[0.0, 9.0]]))[0] == 0.0


def test_4_negative_match_is_possible():
    assert memory_match(np.array([1.0]), np.array([[-2.0]]))[0] == -2.0


def test_5_zero_question_gives_zero_scores():
    np.testing.assert_allclose(memory_match(np.zeros(2), np.ones((3, 2))), 0.0)


def test_6_does_not_mutate_memory():
    M = np.ones((2, 2))
    memory_match(np.ones(2), M)
    np.testing.assert_array_equal(M, np.ones((2, 2)))

