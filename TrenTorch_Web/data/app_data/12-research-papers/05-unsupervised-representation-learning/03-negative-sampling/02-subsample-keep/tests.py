"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/03-negative-sampling/02-subsample-keep/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ns-subsample")
subsample_keep_prob = _module.subsample_keep_prob


import math


def test_1_rare_word_is_always_kept():
    assert subsample_keep_prob(1e-6, 1e-4) == 1.0


def test_2_hand_value_for_frequent_word():
    assert abs(subsample_keep_prob(1e-2, 1e-4) - 0.1) < 1e-12


def test_3_keep_probability_decreases_with_frequency():
    assert subsample_keep_prob(0.5, 1e-3) < subsample_keep_prob(0.01, 1e-3)


def test_4_result_is_in_unit_interval():
    p = subsample_keep_prob(0.3, 1e-4)
    assert 0.0 < p <= 1.0


def test_5_returns_a_python_float():
    assert isinstance(subsample_keep_prob(0.1, 0.01), float)


def test_6_threshold_equal_to_frequency_keeps_everything():
    assert subsample_keep_prob(0.2, 0.2) == 1.0

