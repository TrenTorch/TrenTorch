"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/02-pointer-networks/03-pointer-sequence/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ptr-pointer-sequence")
pointer_argmax_sequence = _module.pointer_argmax_sequence


import numpy as np


def test_1_one_position_per_step():
    assert pointer_argmax_sequence(np.eye(3)) == [0, 1, 2]


def test_2_returns_python_ints():
    assert all(isinstance(i, int) for i in pointer_argmax_sequence(np.ones((2, 2))))


def test_3_single_step():
    assert pointer_argmax_sequence(np.array([[0.2, 0.8]])) == [1]


def test_4_repeated_points_are_allowed():
    assert pointer_argmax_sequence(np.array([[1.0, 0.0], [1.0, 0.0]])) == [0, 0]


def test_5_length_matches_steps():
    assert len(pointer_argmax_sequence(np.zeros((5, 3)))) == 5


def test_6_does_not_mutate_scores():
    s = np.array([[1.0, 2.0]])
    pointer_argmax_sequence(s)
    np.testing.assert_array_equal(s, [[1.0, 2.0]])

