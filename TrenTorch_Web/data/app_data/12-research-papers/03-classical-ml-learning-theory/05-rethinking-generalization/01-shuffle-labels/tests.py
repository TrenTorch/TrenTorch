"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/05-rethinking-generalization/01-shuffle-labels/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-generalization-shuffle-labels")
shuffle_labels = _module.shuffle_labels


import numpy as np


def test_1_keeps_the_same_multiset_of_labels():
    rng = np.random.default_rng(0)
    y = np.array([0, 1, 1, 2])
    np.testing.assert_array_equal(np.sort(shuffle_labels(y, rng)), np.sort(y))


def test_2_keeps_the_length():
    assert len(shuffle_labels(np.arange(7), np.random.default_rng(1))) == 7


def test_3_same_seed_gives_same_permutation():
    y = np.arange(10)
    a = shuffle_labels(y, np.random.default_rng(5))
    b = shuffle_labels(y, np.random.default_rng(5))
    np.testing.assert_array_equal(a, b)


def test_4_usually_changes_the_order():
    y = np.arange(20)
    assert not np.array_equal(shuffle_labels(y, np.random.default_rng(3)), y)


def test_5_single_label_is_unchanged():
    np.testing.assert_array_equal(shuffle_labels(np.array([4]), np.random.default_rng(0)), [4])


def test_6_does_not_mutate_the_input():
    y = np.array([0, 1, 2])
    shuffle_labels(y, np.random.default_rng(2))
    np.testing.assert_array_equal(y, [0, 1, 2])

