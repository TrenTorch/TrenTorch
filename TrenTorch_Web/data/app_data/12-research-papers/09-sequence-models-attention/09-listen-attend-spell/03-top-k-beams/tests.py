"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/09-listen-attend-spell/03-top-k-beams/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-las-top-k-beams")
top_k_beams = _module.top_k_beams


import numpy as np


def test_1_keeps_the_best_hypotheses():
    assert top_k_beams(np.array([-1.0, -0.2, -3.0]), 2) == [1, 0]


def test_2_beam_wider_than_candidates_keeps_all():
    assert sorted(top_k_beams(np.array([0.1, 0.2]), 5)) == [0, 1]


def test_3_beam_of_one_is_the_argmax():
    assert top_k_beams(np.array([0.1, 0.9, 0.5]), 1) == [1]


def test_4_returns_python_ints():
    assert all(isinstance(i, int) for i in top_k_beams(np.array([1.0, 2.0]), 2))


def test_5_ties_keep_the_earlier_index():
    assert top_k_beams(np.array([1.0, 1.0]), 1) == [0]


def test_6_does_not_mutate_scores():
    s = np.array([1.0, 2.0])
    top_k_beams(s, 1)
    np.testing.assert_array_equal(s, [1.0, 2.0])

