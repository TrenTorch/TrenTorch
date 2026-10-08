"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/03-negative-sampling/03-unigram-noise/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ns-unigram-noise")
unigram_noise = _module.unigram_noise


import numpy as np


def test_1_sums_to_one():
    assert abs(unigram_noise(np.array([3.0, 7.0, 1.0])).sum() - 1.0) < 1e-12


def test_2_equal_counts_give_uniform():
    np.testing.assert_allclose(unigram_noise(np.array([5.0, 5.0])), [0.5, 0.5])


def test_3_hand_value_with_power_three_quarters():
    # 16^0.75 = 8, 1^0.75 = 1
    np.testing.assert_allclose(unigram_noise(np.array([16.0, 1.0])), [8 / 9, 1 / 9])


def test_4_more_frequent_words_get_more_mass():
    p = unigram_noise(np.array([10.0, 1.0]))
    assert p[0] > p[1]


def test_5_power_one_is_the_plain_frequency():
    np.testing.assert_allclose(unigram_noise(np.array([1.0, 3.0]), power=1.0), [0.25, 0.75])


def test_6_does_not_mutate_counts():
    c = np.array([2.0, 4.0])
    unigram_noise(c)
    np.testing.assert_array_equal(c, [2.0, 4.0])

