"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

rand_index = load_solution(__file__).rand_index


def test_identical_partitions_score_one():
    labels = np.array([0, 0, 1, 1, 2])
    assert rand_index(labels, labels) == 1.0


def test_relabeling_does_not_change_the_score():
    a = np.array([0, 0, 1, 1, 2, 2])
    b = np.array([7, 7, 3, 3, 9, 9])
    assert rand_index(a, b) == 1.0


def test_hand_computed_value():
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 0, 1])
    # Only pairs (0,3) and (1,2) agree: 2 of 6.
    assert np.isclose(rand_index(a, b), 2 / 6)


def test_symmetric():
    rng = np.random.default_rng(0)
    a, b = rng.integers(0, 3, 20), rng.integers(0, 4, 20)
    assert np.isclose(rand_index(a, b), rand_index(b, a))


def test_matches_pair_loop_oracle():
    rng = np.random.default_rng(1)
    a, b = rng.integers(0, 3, 25), rng.integers(0, 3, 25)
    agree = total = 0
    for i in range(25):
        for j in range(i + 1, 25):
            total += 1
            agree += (a[i] == a[j]) == (b[i] == b[j])
    assert np.isclose(rand_index(a, b), agree / total)


def test_fewer_than_two_samples():
    assert rand_index(np.array([0]), np.array([5])) == 1.0
    assert rand_index(np.array([], dtype=int), np.array([], dtype=int)) == 1.0


def test_range_and_type():
    rng = np.random.default_rng(2)
    value = rand_index(rng.integers(0, 3, 15), rng.integers(0, 3, 15))
    assert isinstance(value, float) and 0.0 <= value <= 1.0
