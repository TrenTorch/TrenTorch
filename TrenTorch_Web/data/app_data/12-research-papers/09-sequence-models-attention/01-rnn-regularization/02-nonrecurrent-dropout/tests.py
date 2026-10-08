"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/01-rnn-regularization/02-nonrecurrent-dropout/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zaremba-nonrecurrent-dropout")
nonrecurrent_dropout = _module.nonrecurrent_dropout


import numpy as np


def test_1_kept_units_are_scaled():
    np.testing.assert_allclose(nonrecurrent_dropout(np.array([1.0, 2.0]), np.array([1, 0]), 0.5), [2.0, 0.0])


def test_2_no_dropout_is_identity():
    h = np.array([3.0, -1.0])
    np.testing.assert_allclose(nonrecurrent_dropout(h, np.ones(2), 0.0), h)


def test_3_all_dropped_gives_zero():
    np.testing.assert_allclose(nonrecurrent_dropout(np.ones(3), np.zeros(3), 0.4), 0.0)


def test_4_keeps_the_shape():
    assert nonrecurrent_dropout(np.ones((2, 3)), np.ones((2, 3)), 0.2).shape == (2, 3)


def test_5_expectation_is_preserved():
    h = np.array([2.0])
    p = 0.5
    expected = 0.5 * nonrecurrent_dropout(h, np.array([1.0]), p) + 0.5 * nonrecurrent_dropout(h, np.array([0.0]), p)
    np.testing.assert_allclose(expected, h)


def test_6_does_not_mutate_input():
    h = np.array([1.0])
    nonrecurrent_dropout(h, np.array([1.0]), 0.5)
    np.testing.assert_array_equal(h, [1.0])

